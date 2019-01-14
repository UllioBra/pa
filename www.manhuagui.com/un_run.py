# import subprocess,time,os,sys
# import Get_Pic_Pro_MutiPrc
# import Get_Pic_Pro

# class AutoRun():
#     def __init__(self, Time, key, url):
#         self.sleep_time = Time
#         self.key = key
#         self.p = None
#         self.url = url
#         self.run()

#         try:
#             while True:
#                 time.sleep(self.sleep_time * float(60))
#                 self.poll = self.p.poll()
#                 if self.poll is None:
#                     print('Good')
#                 else:
#                     print("Bad")
#                     self.run()
#         except KeyboardInterrupt as e:
#             print("Process finished")

#     def run():
#         self.p = subprocess.Popen(['python', '%s' % , '%d' % self.add_a, '%d' %self.add_b], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)

    
