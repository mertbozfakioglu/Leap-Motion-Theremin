// (launch with OSC_send.ck)

// the patch
SinOsc s =>  dac;
//2 => s.sync;

// create our OSC receiver
OscRecv recv;
// use port 6449
9000 => recv.port;
// start listening (launch thread)
recv.listen();
10 => s.freq;
// create an address in the receiver, store in new variable
recv.event( "/test/address, s" ) @=> OscEvent oe;

// infinite event loop
while ( true )
{    
    //float inputs[];
    //splice("-19.8903846741,179.325408936,-112.919670105,109",4) @=> inputs;
    //<<<inputs[0]>>>;
    //<<<inputs[1]>>>;
    //<<<inputs[2]>>>;
    //<<<inputs[3]>>>;
    
    
    // wait for event to arrive
    oe => now;
    while ( oe.nextMsg() != 0 )
    {   
        // getFloat fetches the expected float (as indicated by "f")
        //oe.getFloat() => buf.play;
        // print
        //<<< oe.nextMsg()>>>;
        //<<<oe.getString()>>>;
        
        //x,y,z,roll,grab,pinch
        splice(oe.getString(),6) @=> float inputs[];
        <<<inputs[5]>>>;
        inputs[0]*24+60 => float x;
        Std.mtof(x) => x; 
        inputs[1] * .5 => float y;
        inputs[2] => float z;
        //inputs[3] => float roll;
        //inputs[4] => float grab;
        //inputs[5] => float pinch;
        //<<<x>>>;
        
        

        x => s.freq;
        y => s.gain;
        Std.fabs(z);
        //z*.2 => vib.gain; //0, 30 ayarlanacak
        //.5 => chor.modDepth; 
        // 2 => chor.modFreq;
        10::ms => now;
        
        }
    
}
fun float[] splice( string in , int len)
{
    float inputs[len];
    for (0 => int a ; a < len-1; a++){
        in.find(',') => int i;
        in.substring(0,i).toFloat() => inputs[a];
        in.substring(i+1) => in;
    }
    in.toFloat() => inputs[len-1];
    return inputs;
}
