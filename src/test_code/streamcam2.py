import cv2  # Library for webcam images capturing
import gi   # Library for ip-camera simulation
# Gstreamer requirements
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
# GStreamer classes 
from gi.repository import Gst, GstRtspServer, GObject

#Factory class
class SensorFactory(GstRtspServer.RTSPMediaFactory):  
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)  # Init super class
        print("Start GST Server")
        self.cap = cv2.VideoCapture(0)  # Initialize webcam. You may have to change 0 to your webcam number
        print("cam : ", self.cap)
        self.frame_number = 0  # Current frame number
        self.fps = 10  # output streaming fps
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME caps=video/x-raw,format=BGR,width=640,height=480,framerate={}/1 !\
            videoconvert ! video/x-raw,format=I420 ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay config-interval=1 \
            name=pay0 pt=96'.format(self.fps)
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)  # Launch gst plugin
    def do_configure(self, rtsp_media):
        self.frame_number = 0  # Set current frame number to zero
        appsrc = rtsp_media.get_element().get_child_by_name('source')  # get source from gstreamer
        appsrc.connect('need-data', self.on_need_data)  # set data provider
    def on_need_data(self, src, lenght):
        if self.cap.isOpened():  # Check webcam is opened
            ret, frame = self.cap.read()  # Read next frame
            frame = self.draw_on_frame(frame)  # Draw something on frame frame
            
            if ret:  # If read success
                data = frame.tostring()  # Reformat frame to string
                buf = Gst.Buffer.new_allocate(None, len(data), None)  # Allocate memory
                buf.fill(0, data)  # Put new data in memory
                buf.duration = self.duration  # Set data duration
                timestamp = self.frame_number * self.duration  # Current frame timestamp
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp  # Set frame timestamp
                self.frame_number += 1  # Increase current frame number
                retval = src.emit('push-buffer', buf)  # Push allocated memory to source container
                if retval != Gst.FlowReturn.OK:  # Check pushing process
                    print(retval)  # Print error message

    def draw_on_frame(self, frame):
        cv2.waitKey(1)
        return frame  # Just return frame without changes


# Server class
class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)  # Init super class
        self.factory = SensorFactory()  # Create factory
        self.set_service("3002")  # Set service port
        self.factory.set_shared(True)  # Set shared to true
        self.get_mount_points().add_factory("/test", self.factory)  # Add routing to access factory
        self.attach(None)

if __name__ == '__main__':
    # Create infinite loop for gstreamer server
    loop = GObject.MainLoop() 
    # Initialize server threads for asynchronous requests 
    GObject.threads_init()  
    # Initialize GStreamer
    Gst.init(None)  
    
    server = GstServer()  # Initialize server
    loop.run()  # Start infinite loop
