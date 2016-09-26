import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import OSC
c = OSC.OSCClient()
c.connect(('127.0.0.1', 9000))   # connect to SuperCollider

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
        for hand in frame.hands:
            print "hand"
            x = hand.pointables.frontmost.tip_position.x 
            y = hand.pointables.frontmost.tip_position.y
            z = hand.pointables.frontmost.tip_position.z
            roll = hand.palm_normal.roll
            angle = int(90 - roll*60)
            
            oscmsg = OSC.OSCMessage()
            oscmsg.setAddress("/test/address")
            oscmsg.append(str(x)+","+str(y)+","+str(z)+","+str(angle))
            c.send(oscmsg)
            
            print str(x)

            
            #oscmsg.append(str(y))
            #oscmsg.append(str(z))
            #oscmsg.append(str(angle))

            
            

            
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
            #print (x,y,z,velocity,angle)

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
