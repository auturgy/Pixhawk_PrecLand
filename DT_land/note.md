fake GPS message in order to maintain the position without GPS ( due to my GPS's poor result ).

1. check message_factory if it does have the desired fake GPS function
https://discuss.ardupilot.org/t/feed-copter-gps-updates-from-companion-computer/14097

# CODE:
connect code;
set appropriate parameters, ready for Precision Loiter and Precision Land;
openCV initialization;

while 1{
  if 1450<=RC_mode<=1550
  {

  }
  else // Not use RC override, control manually!
  {
    release all channels;
  }
}

2. RC failsafe -> using other channels.
