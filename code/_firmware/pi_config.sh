#!/bin/bash

# --- Configure SSH ---
echo "Enable SSH..."
sudo raspi-config nonint do_ssh 0
echo "SSH enabled."

# --- Configure I2C ---
echo "Enabling I2C..."
sudo raspi-config nonint do_i2c 0
echo "I2C enabled."

# --- Configure VNC ---
echo "Enabling VNC..."
sudo raspi-config nonint do_vnc 0
echo "VNC enabled."

# --- Configure GPIO ---
echo "Enabling GPIO..."
sudo raspi-config nonint do_rgpio 0
echo "Remote GPIO enabled."

echo "Installing i2c-tools and python-smbus"
sudo apt install -y i2c-tools python-smbus
echo "i2c-tools and smbus installed"

echo "Installing Adafruit Servo-Kit..."
pip3 install adafruit-circuitpython-servokit
echo "Adafruit Servo-Kit installed."

echo "Installing Accelerometer...."
pip3 install mpu6050-raspberrypi --break-system-packages
echo "Accelerometer installed."
