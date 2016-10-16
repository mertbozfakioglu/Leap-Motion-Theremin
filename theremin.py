import sys, math, time
#src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
#arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
#sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import OSC
c = OSC.OSCClient()
c.connect(('127.0.0.1', 9000))   # connect to SuperCollider

debug = False

class SampleListener(Leap.Listener):
    """
    c = OSC.OSCClient()
    c.connect(('127.0.0.1', 57120))   # connect to SuperCollider
    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/startup")
    oscmsg.append('HELLO')
    c.send(oscmsg)
    """
    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
        print "Frame available"


    def on_frame(self, controller):
        
        #oscmsg.append('HELLO')
        #c.send(oscmsg)
        print "Frame available"
        #screen.blit(background,(0,0)) 
        #pygame.draw.rect(screen,(255,255,255),Rect(192,39,640,640),3)
        frame = controller.frame()
        print "frame"
        if frame.hands.is_empty and not debug:
            oscmsg = OSC.OSCMessage()
            oscmsg.setAddress("/test/address")
            oscmsg.append("0.0,0.0,0.0,0.0,0.0,0.0")
            c.send(oscmsg)
        for hand in frame.hands:
            print "hand"
            #x = hand.pointables.frontmost.tip_position.x 
            #y = hand.pointables.frontmost.tip_position.y
            #z = hand.pointables.frontmost.tip_position.z
            roll = hand.palm_normal.roll
            angle = int(90 - roll*60)
            grab = hand.grab_strength
            thumb =  hand.fingers.finger_type(0)[0]
            index =  hand.fingers.finger_type(1)[0]

            x = index.tip_position.x
            y = index.tip_position.y
            z = index.tip_position.z

            dist = index.tip_position-thumb.tip_position
            pinch = math.sqrt(dist[0]**2+dist[1]**2+dist[2]**2)
            pinch = (pinch-25)/75
            if pinch>1:
                pinch = 1
            elif pinch<0:
                pinch = 0

            #print pinch
            """
            sphere = hand.sphere_radius   
            sphere = (sphere-40)/150
            if sphere>1:
                sphere = 1
            elif sphere<0:
                sphere = 0
                """
            roll = roll/6+0.5
            if roll>1:
                roll = 1
            elif roll<0:
                roll = 0
            #print roll

            x = (x+300)/600
            if x>1:
                x = 1
            elif x<0:
                x = 0

            y = (y-130)/370
            if y>1:
                y = 1
            elif y<0:
                y = 0            

            if not debug:
            	oscmsg = OSC.OSCMessage()
            	oscmsg.setAddress("/test/address")
            	oscmsg.append(str(x)+","+str(y)+","+str(z)+","+str(roll)+","+str(grab)+","+str(pinch))
            	c.send(oscmsg)
            
            #print str(y)
            #print str(x)            
            
            if angle>180:
                angle = 180
            elif angle<0:
                angle = 0
            radius = hand.sphere_radius
            velocity = int(radius*0.9-40)
            if velocity>180:
                velocity = 180
            elif velocity<10:
                velocity = 0
            #Slow down the code to evoid accumulation of messages on the ChucK side 
            time.sleep(0.01)
def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
