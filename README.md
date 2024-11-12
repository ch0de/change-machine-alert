If you own Laundromats. Car wash, Arcade or anything with a change machine you know how important it is to know when your machine is of of order. Older machines do not have this built in. So I made a simple circuit using a Raspberry pi Pico W and a relay that monitors the Out OF Order light and sends a text And/Or e-mail when the light is on.

Parts
Raspberry Pi Pico W https://a.co/d/6opDsDU

relay (type depends on your change machine brand) For my 24v standard https://a.co/d/4sleMeM my 120v hamilton https://a.co/d/9Oh8v2h

Wire Splicers https://a.co/d/gxGjUzP

Soldering Iron https://a.co/d/9EdydSx

electrical wire https://a.co/d/6snHIRc

Wifi at your location.

step 1 
Figure Out What Type of Out of Order Light You Have
turn on the Out of order light and Use a MultiMeter and test the voltage of your out of order light. also which wire is + and Which is Ground.

My Old Hamiltons are 120v AC

My Old Standard with a replacement Controller is 24vDC

Yours may be different, and what relay you buy will depend what your voltage is.

Step 2: Connect Out of Order Light to Relay
using Wire Taps, Tap into the + Side of the Out of order light and run it to the + side of the relay input

And The negative to negative. On some relays you may need to also Jumper from the + to the "In"

Step 3: Connect Relay to Pi Pico W
Connect a line from "NO" (Normally Open) on the realy to Pin 4 on the Pi Pico W.

Connect a line from "Com" (common) on the realy to any Ground pin on the pico.

If you have two change machines side by side you can install a Relay in that one also and Run wire (i use old network or phone wire) between them and connect the second machine "NO" to Pin 4, and "Com" to any "G" pin.


Step 4: Program Pi Pico
First update the firmware of the Pi Pico w https://a.co/d/6snHIRc

Download and install Thonny https://thonny.org/

using thonny (ask Chatgpt) Upload umail.py to the Pico

open main.py

Lines 16 to 18 change your SSID, and Wifi password. make sure to keep it between the ` `

lines 20 to 25 enter your smtp server username password

line 25 you can enter as many email addresses as you like, Separated by a comma ,

if you want it to text your phone also you will have to find your Cell phone carriers email to text address. Example .For at&t it is phonenumber@txt.att.net



This code also is set to check each Pin every 5 seconds, If a pin is triggered, an alert is sent, and that pin is ignored for 1 hour, after 1 hour it will send another email and ignore for another hour until the Out of order is reset.
