"""=====================================================
Board Burner Club

# Created by James J. Smith 11/9/2024

# Restructured by Andrew G. Sahm 3/21/2025
    This file is the ai agent but also the game rolled into one application
    This sends the action to the middlware to perform, and receives the
    state from the middleware. It sends the state to the AI for a new predicted
    action.

    This is also where the reward system and the training steps are defined 

====================================================="""
import torch
import random
import numpy as np
import time
import colorsys
from collections import deque
from ai_tasks.ai_models.ai_model import Linear_QNet, QTrainer 

DEBUG_PRINT_MOVE_DECISION = True           # predicted or random action decision
DEBUG_PRINT_MOVE_DECISION_NUMBERS = False   # number of predicted vs random moves per game
DEBUG_PRINT_REWARD = False                  # reward for every action
DEBUG_PRINT_STATE_VARIABLE = True          # entire state variable every loop
DEBUG_PRINT_BALL_LOCATION = False           # new ball location when moved
DEBUG_PRINT_PREDITION_RAW_NUMBER = False    # raw ai data for predictions
DEBUG_PRINT_AI_SETTINGS = True              # header info with settings
DEBUG_PRINT_BALL_VISIBILITY = True          # whether the puck sees the ball

EXPLORATION_NUMBER_OF_GAMES = 200

TIME_PER_GAME = 60
PERCENT_ARRAY_FULL = 30
PING_PONG_BALL_COUNT = 7
PING_PONG_BALL_PLACE_RADIUS = 0.6

MAX_MEMORY = 10_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

NUMBER_OF_SEGMENTS = 8  # used to convert camera width into small array

# regular lighting (hMin = 0 , sMin = 0, vMin = 67), (hMax = 162 , sMax = 21, vMax = 175)
#WALL_MIN_HSV = [0, 0, 0]
#WALL_MAX_HSV = [179, 255, 255]

WALL_MIN_HSV = [0, 0, 0]
WALL_MAX_HSV = [179, 255, 255]

# regular lighting {'hMin': 68, 'sMin': 113, 'vMin': 15, 'hMax': 87, 'sMax': 255, 'vMax': 116}
# poor lighting {'hMin': 37, 'sMin': 131, 'vMin': 0, 'hMax': 79, 'sMax': 255, 'vMax': 161}
GREEN_BALL_MIN_HSV = [13, 50, 0]
GREEN_BALL_MAX_HSV = [79, 255, 75] # green ball

BLUE_BALL_MIN_HSV = [88, 102, 35]
BLUE_BALL_MAX_HSV = [145, 255, 255] # blue ball

CAMERA_WIDTH = 160
CAMERA_HEIGHT = 120

class Find_Ball:

    def __init__(self, input_size):
        #self.robot = Supervisor()

        self.num_of_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.8 # discount rate must be smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()

        self.final_move = [0, 0, 0, 0]      # Forward, Left, Right, Stop
        self.distance = 0

        self.reward = 0
        self.score = 0
        self.record = 0
        self.was_ball_visible_last_state = 0
        self.number_of_collide_wall_pixels = 0

        self.num_of_random_moves = 0
        self.num_of_predicted_moves = 0
        self.loop_count = 0

        self.is_colliding = False
        self.cause_of_death = None

        self.start_time = time.time()
        self.elapsed_time = time.time()

        self.input_layer_size = input_size
        self.hidden_layer_size = int(2/3 * self.input_layer_size) + len(self.final_move)  # 2/3 size of state variable + output size 

        self.model = Linear_QNet(self.input_layer_size, self.hidden_layer_size, len(self.final_move))
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

        self.num_layers = self.model.getNumberOfHiddenLayers()

        if DEBUG_PRINT_AI_SETTINGS:
            self.printAISettings()

    def new(self):
        pass

    def printAISettings(self):
        print("Number of Exploration Games: ", str(EXPLORATION_NUMBER_OF_GAMES))
        print("State Size : ", str(self.input_layer_size))
        print("Hidden Layer Size: ", str(self.hidden_layer_size), "Number of Hidden Layers: ", str(self.num_layers))
        print("Max Memory: ", str(MAX_MEMORY), "  Batch Size: ", str(BATCH_SIZE))
        print("Learning Rate: ", str(LEARNING_RATE))

    def resetGame(self):
        self.start_time = time.time()

        if DEBUG_PRINT_MOVE_DECISION_NUMBERS:
            if self.num_of_predicted_moves != 0:
                print("Number of Random Moves : ", str(self.num_of_random_moves), "Number of Predicted Moves : ", str(self.num_of_predicted_moves))
                print("Percent of Predicted Moves : ", str(self.num_of_predicted_moves / (self.num_of_predicted_moves + self.num_of_random_moves) * 100.0))

        self.num_of_random_moves = 0
        self.num_of_predicted_moves = 0

        self.is_colliding = False

    def getScore(self):
        if self.number_of_green_pixels > int(NUMBER_OF_SEGMENTS*PERCENT_ARRAY_FULL/100):
            self.score += 1
            self.start_time = time.time()

        elif self.number_of_wall_pixels == NUMBER_OF_SEGMENTS:
            self.is_colliding = True

        else:
            pass

        return self.score
    
    def convertMovetoButton(self, move):
        idx = 0
        for m in move:
            if m == 1:
                break
        
            idx += 1

        if idx == 0:
            button = "walk_forward"
        elif idx == 1:
            button = "turn_left"
        elif idx == 2:
            button = "turn_right"
        else:
            button = "stand"

        return button
    
    def getGameData(self, move, state):
        self.reward = self.getReward(state)
        self.score = self.getScore()

        if DEBUG_PRINT_STATE_VARIABLE:
            print("State :" + str(state))

        if DEBUG_PRINT_REWARD:
            print("Reward " + str(self.reward))

        button = self.convertMovetoButton(move)

        self.elapsed_time = time.time() - self.start_time
        if self.elapsed_time > TIME_PER_GAME:
            alive = False
            self.reward = -4000
            self.cause_of_death = "Timeout"

        elif self.is_colliding:
            alive = False
            self.reward = -4000
            self.cause_of_death = "Wall"

        else:
            alive = True

        return button, alive, self.score, self.reward 

    def determineCauseOfDeath(self):
        return self.cause_of_death
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if max memory is reached

    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def trainShortMemory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def predictMove(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = EXPLORATION_NUMBER_OF_GAMES - self.num_of_games  # More games mean smaller epsilon

        if self.epsilon < 20:
            self.epsilon = 20

        # Reset final move to 0s
        for k in range(len(self.final_move)):
            self.final_move[k] = 0

        if random.randint(0, 2.5*EXPLORATION_NUMBER_OF_GAMES) < self.epsilon:
            move = random.randint(0, len(self.final_move)-1)
            self.final_move[move] = 1
            move_buffer = "Random "
            self.num_of_random_moves += 1

        else:
            state0  = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) # can be raw value [5.0, 2.7, 0.1, 0.4]
            
            if DEBUG_PRINT_PREDITION_RAW_NUMBER:
                print("Prediction : " + str(prediction))

            move = torch.argmax(prediction).item() # find idx of max
            self.final_move[move] = 1 # set to [1, 0, 0, 0]
            move_buffer = "Predicted "
            self.num_of_predicted_moves += 1

        if DEBUG_PRINT_MOVE_DECISION:
            print(move_buffer + "Move Decision  : " + str(self.final_move))

        return self.final_move
    
    def getReward(self, state):
        reward = 0
        is_ball_visible_current_state = 0 
        self.number_of_green_pixels = 0
        self.number_of_empty_pixels = 0
        self.number_of_wall_pixels = 0
        self.number_of_collide_wall_pixels = 0
        is_driving_forward = False
        is_stopped = False
        is_turning = False
        is_ball_centered = False

        if state[24] == state[25] and state[24] > 0:
            is_driving_forward = True
            is_stopped = False
            is_turning = False

        elif state[24] == state[25] and state[24] == 0:
            is_driving_forward = False
            is_stopped = True
            is_turning = False

        else:
            is_driving_forward = False
            is_stopped = False
            is_turning = True

        # green ball detection
        for s in state[:2]:
            if s == 1:
                reward += 20
                self.number_of_green_pixels += 1


            else:
                self.number_of_empty_pixels += 1

        for s in state[2:3]:
            if s == 1:
                reward += 60
                self.number_of_green_pixels += 1

            else:
                self.number_of_empty_pixels += 1

        for s in state[3:5]:
            if s == 1:
                reward += 200
                self.number_of_green_pixels += 1
                is_ball_centered = True

            else:
                self.number_of_empty_pixels += 1

        for s in state[5:6]:
            if s == 1:
                reward += 60
                self.number_of_green_pixels += 1

            else:
                self.number_of_empty_pixels += 1

        for s in state[6:8]:
            if s == 1:
                reward += 40
                self.number_of_green_pixels += 1

            else:
                self.number_of_empty_pixels += 1

        # was ball visible
        if self.number_of_green_pixels > 0:
            is_ball_visible_current_state = 1

        # white wall detection
        for s in state[8:16]:
            if s == 1:
                self.number_of_wall_pixels += 1

        for s in state[16:24]:
            if s == 1:
                self.number_of_collide_wall_pixels += 1

        # If no green ball, reward for spinning
        if not is_ball_visible_current_state and is_turning:
            reward += 30

        if not is_ball_visible_current_state and is_stopped:
            reward -= 100

        if self.number_of_wall_pixels > 0:
            reward -= 10    # if no wall pixels still negative
            for x in range(self.number_of_wall_pixels):
                reward -= 10

        # more stringent constraint, if no ball, and sees wall, and driving forward
        if not is_ball_visible_current_state and is_driving_forward :
            reward -= 10   

        # more stringent constraint, if no ball, and sees wall, and driving forward
        if not is_ball_visible_current_state and is_stopped:
            reward -= 100    # if no wall pixels still negative

        # if green ball, reward for driving forward
        if is_ball_visible_current_state and is_driving_forward:
            reward += 1000

        if is_ball_centered and is_driving_forward:
            reward += 500

        if is_ball_visible_current_state and is_stopped:
            reward += 30

        # compare if ball was visible between last state and current state
        if self.was_ball_visible_last_state and not is_ball_visible_current_state:
            reward -= 1000
            if DEBUG_PRINT_BALL_VISIBILITY:
                print("Ball was lost")

        elif not self.was_ball_visible_last_state and is_ball_visible_current_state:
            reward += 50
            if DEBUG_PRINT_BALL_VISIBILITY:
                print("Ball was found")

        # if ball captured
        if self.number_of_green_pixels > int(NUMBER_OF_SEGMENTS*PERCENT_ARRAY_FULL/100):
            reward = 2400   #overwrite all other rewards

        self.was_ball_visible_last_state = is_ball_visible_current_state

        return reward
    
    def getBallImageState(self, camera_buffer, color):
        hsv_camera_buffer = []
        green_array = []    
        #print(camera_buffer.shape)
        #print(camera_buffer)

        if color == "green":
            ball_min_hsv = GREEN_BALL_MIN_HSV
            ball_max_hsv = GREEN_BALL_MAX_HSV
        elif color == "blue":
            ball_min_hsv = BLUE_BALL_MIN_HSV
            ball_max_hsv = BLUE_BALL_MAX_HSV
        else:
            ball_min_hsv = GREEN_BALL_MIN_HSV
            ball_max_hsv = GREEN_BALL_MAX_HSV

        for j in range(int(CAMERA_HEIGHT)):
            r = camera_buffer[j][0]
            g = camera_buffer[j][1]
            b = camera_buffer[j][2]

            hsv_camera_buffer = colorsys.rgb_to_hsv(r, g, b) 
            if hsv_camera_buffer[0]*100 > ball_min_hsv[0] and hsv_camera_buffer[0]*100 <= ball_max_hsv[0] and hsv_camera_buffer[1]*100 > ball_min_hsv[1] and hsv_camera_buffer[1]*100 <= ball_max_hsv[1] and hsv_camera_buffer[2] > ball_min_hsv[2] and hsv_camera_buffer[2] <= ball_max_hsv[2]:
                green_array.append(1)
            else:
                green_array.append(0)  

        return green_array 

    def getWallImageState(self, camera_buffer):
        hsv_camera_buffer = []
        wall_array = []

        for j in range(int(CAMERA_HEIGHT)):
            r = camera_buffer[j][0]
            g = camera_buffer[j][1]
            b = camera_buffer[j][2]

            hsv_camera_buffer = colorsys.rgb_to_hsv(r, g, b) 
            if hsv_camera_buffer[0]*100 >= WALL_MIN_HSV[0] and hsv_camera_buffer[0]*100 <= WALL_MAX_HSV[0] and hsv_camera_buffer[1]*100 >= WALL_MIN_HSV[1] and hsv_camera_buffer[1]*100 <= WALL_MAX_HSV[1]  and hsv_camera_buffer[2] >= WALL_MIN_HSV[2] and hsv_camera_buffer[2] <= WALL_MAX_HSV[2]:
                wall_array.append(1)
            else:
                wall_array.append(0) 

        return wall_array 

    def convertArraytoSmallerSegments(self, pixel_array):
        temp_state = pixel_array
        small_state = []

        for k in range(NUMBER_OF_SEGMENTS):
            small_state.append(0)

        number_per_segment = int(len(temp_state) / NUMBER_OF_SEGMENTS)

        for k in range(NUMBER_OF_SEGMENTS):
            for j in range(number_per_segment):
                if temp_state[0] == 1:
                    small_state[k] = 1
                temp_state.pop(0)
            
        return small_state
    
    def getBallFilteredFrame(self, frame):
        height = frame.shape[0]
        width = frame.shape[1]

        filtered = np.zeros((height, width), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                r = frame[y][x][0]
                g = frame[y][x][1]
                b = frame[y][x][2]

                hsv_buffer = colorsys.rgb_to_hsv(r, g, b)
                #print(hsv_buffer[0]*100, hsv_buffer[1]*100, hsv_buffer[2])
                if hsv_buffer[0]*100 >= GREEN_BALL_MIN_HSV[0] and hsv_buffer[0]*100 <= GREEN_BALL_MAX_HSV[0] and hsv_buffer[1]*100 >= GREEN_BALL_MIN_HSV[1] and hsv_buffer[1]*100 <= GREEN_BALL_MAX_HSV[1]  and hsv_buffer[2] >= GREEN_BALL_MIN_HSV[2] and hsv_buffer[2] <= GREEN_BALL_MAX_HSV[2]:
                    filtered[y][x] = 255   # white pixel
                else:
                    filtered[y][x] = 0     # black pixel

        return filtered
    
    def getWallFilteredFrame(self, frame):
        height = frame.shape[0]
        width = frame.shape[1]

        filtered = np.zeros((height, width), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                r = frame[y][x][0]
                g = frame[y][x][1]
                b = frame[y][x][2]

                hsv_buffer = colorsys.rgb_to_hsv(r, g, b)
                #print(hsv_buffer[0]*100, hsv_buffer[1]*100, hsv_buffer[2])
                if hsv_buffer[0]*100 >= WALL_MIN_HSV[0] and hsv_buffer[0]*100 <= WALL_MAX_HSV[0] and hsv_buffer[1]*100 >= WALL_MIN_HSV[1] and hsv_buffer[1]*100 <= WALL_MAX_HSV[1]  and hsv_buffer[2] >= WALL_MIN_HSV[2] and hsv_buffer[2] <= WALL_MAX_HSV[2]:
                    filtered[y][x] = 255   # white pixel
                else:
                    filtered[y][x] = 0     # black pixel

        return filtered
    #def getWallFilteredFrame(self):
    #    return self.wall_filter_buffer

"""
if __name__ == "__main__":
    # -----------------------------
    # CONFIGURATION
    # -----------------------------
    INPUT_SIZE = 26  # <-- set this to your actual state size
    USE_DETERMINISTIC_POLICY = True  # disables epsilon randomness

    # -----------------------------
    # INITIALIZE AGENT
    # -----------------------------
    agent = Find_Ball(INPUT_SIZE)

    # Disable exploration randomness if desired
    if USE_DETERMINISTIC_POLICY:
        agent.epsilon = 0

    # Load trained model
    loaded = agent.model.load("model.pth")
    print("Model loaded:", loaded)

    # -----------------------------
    # MAIN INFERENCE LOOP
    # -----------------------------
    print("Starting inference-only run...")

    while True:
        # 1. Get state from your middleware / sensors
        # Replace this with your actual state retrieval function
        state = get_state_of_robot()

        # 2. Predict next move (no training)
        move = agent.predictMove(state)

        # 3. Convert move to robot command + evaluate game status
        button, alive, score, reward = agent.getGameData(move, state)

        # 4. Send action to robot/middleware
        send_action_to_robot(button)

        # 5. Handle episode termination
        if not alive:
            print("\n--- EPISODE ENDED ---")
            print("Cause of death:", agent.determineCauseOfDeath())
            print("Final score:", score)
            print("----------------------\n")

            agent.resetGame()
            time.sleep(0.5)  # small pause before restarting
"""