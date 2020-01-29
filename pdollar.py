import sys
import os
from engine import recognizer
from argparse import ArgumentParser
import datetime 
GESTURE_FOLDER_NAME = "gestureFiles"
class Classifier:
    def __init__(self):
        self.gestureFolder = os.path.join(os.getcwd(), GESTURE_FOLDER_NAME)
        self.trainingSet = self.LoadTrainingSet()

    def RecognizeEventFile(self, fileName):
        try:
            gFile = open(fileName, "r")                
        except IOError:
            pass
        currentStrokeIndex = -1
        points = []
        gestureName = ""
        for line in gFile.readlines():
            line = line.strip('\n')
            if line == "MOUSEDOWN":
                currentStrokeIndex = currentStrokeIndex + 1
            elif line == "RECOGNIZE":
                candidate = recognizer.Gesture(points, gestureName)
                self.RecognizeGesture(candidate)
            elif line != "MOUSEUP":
                x, y = line.split(',')
                points.append(recognizer.Point(float(x),float(y),currentStrokeIndex))
        gFile.close()

    def RecognizeGesture(self, candidate):
        #candidate = recognizer.Gesture()
        gestureClass = recognizer.PointCloudRecognizer().Classify(candidate, self.trainingSet)
        print(gestureClass)
    def LoadTrainingSet(self):
        # /// <summary>
        # /// Loads training gesture samples from XML files
        # /// </summary>
        # /// <returns></returns>
        if not os.path.isdir(self.gestureFolder):
            os.mkdir(self.gestureFolder)
        gestures = []
        io = IOUtility()
        for fileName in os.listdir(self.gestureFolder):
            filePath = os.path.join(self.gestureFolder, fileName)
            gestures.append(io.ReadGesture(filePath))
        return gestures
class IOUtility:
    """
    
    """
    def __init__(self):
        self.gestureFolder = os.path.join(os.getcwd(), GESTURE_FOLDER_NAME)
        self.timeOfTemplate = datetime.datetime.today().strftime("%d-%B-%Y-%H-%M-%S")+"-"+str(datetime.datetime.today().microsecond)
    
    def ReadGesture(self, fileName):
        # /// Reads a multistroke gesture from an XML file
        # /// </summary>
        # /// <param name="fileName"></param>
        # /// <returns></returns>
        points = []
        gestureName = ""
        currentStrokeIndex = -1
        try:
            gFile = open(fileName, "r")                
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
        gFile.close()
        return recognizer.Gesture(points, gestureName)
    
    def WriteGesture(self, points, gestureName, fileName):
        # /// <summary>
        # /// Writes a multistroke gesture to an XML file
        # /// </summary>
        currentStrokeIndex = -1
        try:
            gFile = open(fileName, "w")
        except IOError:
            pass
        gFile.write(gestureName)
        for i in range(len(points)):
            if points[i].StrokeID != currentStrokeIndex:
                if i > 0:
                    gFile.write("END\n")    
                gFile.write("BEGIN\n")
                currentStrokeIndex = points[i].StrokeID
            gFile.write(f"{points[i].X},{points[i].Y}\n")
        gFile.write("END\n")
        gFile.close()
    def SaveGesture(self, fileName):
        # /// <summary>
        # /// Save gesture points to folder as a txt file
        # /// </summary>
        # /// <param name="fileName"></param>
        template = self.ReadGesture(fileName)
        if not os.path.isdir(self.gestureFolder):
            os.mkdir(self.gestureFolder)
        # fileCount = self.fileCounter
        newFileName = fileName.strip(".txt") + "-" + self.timeOfTemplate + ".txt"
        filePath = os.path.join(self.gestureFolder, newFileName)
        # while os.path.exists(filePath):
        #     fileCount = fileCount + 1
        #     newFileName = fileName.strip(".txt") + str(fileCount).rjust(3, fileCount) + ".txt"
        #     filePath = os.path.join(self.gestureFolder, newFileName)

        self.WriteGesture(template.Points, template.Name, filePath)
    
    def ClearTemplates(self):
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
        #io = IOUtility()
        if subcommand == 'help' or self.argv[1:] in (['--help'], ['-h']):
            parser.print_help()
        else:
            if subcommand == '-r':
                # Clears the template
                IOUtility().ClearTemplates
            elif subcommand == '-t':
                IOUtility().SaveGesture(options.gesturefile)
            else:
                # <eventstream>
                # Prints the name of gestures as they are recognized from the event stream
                Classifier().RecognizeEventFile(options.EVENTSTREAM)
                #print(options.EVENTSTREAM)

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