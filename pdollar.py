import sys
from engine import recognizer
from argparse import ArgumentParser

class IOUtility:
    """
    
    """
    def __init__(self):
        pass
    def ReadGesture(self, filename):
        # /// Reads a multistroke gesture from an XML file
        # /// </summary>
        # /// <param name="fileName"></param>
        # /// <returns></returns>
        points = []
        gestureName = ""
        currentStrokeIndex = -1
        try:
            gFile = open(filename, "r")                
        except IOError:
            pass
        lines = gFile.readlines()
        gestureName = lines[0]
        for i in range(1, len(lines)):
            lines[i] = lines[i].strip('\n')
            if lines[i] == "BEGIN":
                currentStrokeIndex = currentStrokeIndex + 1
            elif lines[i] != "END":
                x, y = lines[i].split(',')
                points.append(recognizer.Point(float(x),float(y),currentStrokeIndex))
        return recognizer.Gesture(points, gestureName)
    def AddToTemplates(self, currentTemplates, newTemplate):
        return currentTemplates

    def SaveGesture(self, gestureName):
        pass
    def LoadTrainingSet(self):
        pass

class ManagementUtility:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
    def Execute(self):
        try:
            subcommand = sys.argv[1]
        except:
            subcommand = 'help'

        parser = ArgumentParser()
        #parser.add_argument('args', nargs='*') # catch-all
        parser.add_argument('-t', metavar='<gesturefile>', dest='gesturefile', help="Adds the gesture file to the list of gesture templates.") # adds the gesture file to the list of gesture template
        parser.add_argument('-r', action='store_const', const='clear', dest='clear', help="Clears the templates.") #clears the templates
        parser.add_argument('EVENTSTREAM', nargs='?', metavar='<eventstream>', help="Prints the name of gestures as they are recognized from the event stream.")

        self.parser = parser
        try:
            options, args = parser.parse_known_args(self.argv[1:])
        except:
            pass  # Ignore any option errors at this point.
        io = IOUtility()
        if subcommand == 'help' or self.argv[1:] in (['--help'], ['-h']):
            parser.print_help()
        else:
            if subcommand == '-r':
                print(options.clear)
                # Clears the template
            elif subcommand == '-t':
                io.ReadGesture(options.gesturefile)
            else:
                # <eventstream>
                # Prints the name of gestures as they are recognized from the event stream
                print(options.EVENTSTREAM)

if __name__ == "__main__":
    #print(sys.argv[:])
    utility = ManagementUtility(sys.argv)
    utility.Execute()
    # print(recognizer.Point(1,2,1))
    # a = recognizer.Point(1,2,1)
    # b = recognizer.Point(4,6,2)
    # A = [a]
    # B = [b]
    # print (recognizer.PointCloudRecognizer.CloudDistance(A,B,0))
    # print (recognizer.Geometry.EuclideanDistance(a,b))
    pass