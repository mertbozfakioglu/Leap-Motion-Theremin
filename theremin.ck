// (launch with OSC_send.ck)

// the patch
SinOsc s => dac;


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
    oe => now;    // grab the next message from the queue. 
    
    while ( oe.nextMsg() != 0 )
    {   
        // getFloat fetches the expected float (as indicated by "f")
        //oe.getFloat() => buf.play;
        // print
        //<<< oe.nextMsg()>>>;
        //<<<oe.getString()>>>;
        float inputs[];
        splice(oe.getString(),4) @=> inputs;
        
        //x
        <<<inputs[0]>>>;
        //y
        <<<inputs[1]>>>;
        //z
        <<<inputs[2]>>>;
        //angle
        <<<inputs[3]>>>;
        
        inputs[0] * 990 + 10 => float x;
        inputs[1] => float y;

        <<<x>>>;

        x => s.freq;
        y => s.gain;
        10::ms => now;
    }
    
}
fun float[] splice( string in , int len)
{
    float inputs[4];
    for (0 => int a ; a < len-1; a++){
       in.find(',') => int i;
       in.substring(0,i).toFloat() => inputs[a];
       in.substring(i+1) => in;
    }
    in.toFloat() => inputs[len-1];
    return inputs;
}
