/*
 * Clock Microstepping demo
 *
 * Moves the stepper motor like the seconds hand of a watch.
 *
 * Copyright (C)2015-2017 Laurentiu Badea
 *
 * This file may be redistributed under the terms of the MIT license.
 * A copy of this license has been included with this distribution in the file LICENSE.
 */
#include <Arduino.h>

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
long MOTOR_STEPS = 60000;

// Microstepping mode. If you hardwired it to save pins, set to the same value here.
#define MICROSTEPS 64

#define DIR 5
#define STEP 2
#define SLEEP 8 // optional (just delete SLEEP from everywhere if not used)

/*
 * Choose one of the sections below that match your board
 
 
 */


int enablePin = 8;
#include "BasicStepperDriver.h" // generic
BasicStepperDriver stepper(MOTOR_STEPS, DIR, STEP);

void setup() {
    /*
     * Set target motor RPM=1
     */
     pinMode(enablePin,OUTPUT);
    stepper.begin(1, MICROSTEPS);

    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
    stepper.setEnableActiveState(LOW);
    digitalWrite(enablePin, LOW);
}

void loop() {
    /*
     * The easy way is just tell the motor to rotate 360 degrees at 1rpm
     */
    stepper.rotate(360);
}
