import numpy as np

BIT_RATE = [500.0,850.0,1200.0,1850.0]

class Algorithm:
    def __init__(self):
        self.buffer_size = 0
        self.last_bitrate = 0

    # Intial
    def Initial(self):
        return self.get_params()

    def calculate_bitrate_index(self, S_send_data_size, S_time_interval, S_buffer_size):

        if np.sum(S_time_interval[-1]) > 0:
            throughput_value = np.sum(S_send_data_size[-1]) / np.sum(S_time_interval[-1]) # how many bits per second
        else:
            throughput_value = 999999999999
        bit_rate_Chosen = False
        K = 1070
        for i in range(2, -1, -1):              
            if(S_buffer_size[-1] > K * BIT_RATE[i]  / throughput_value): # S_buffer_size means remain buffer size
                bit_rate = i + 1
                bit_rate_Chosen = True
                break

        if (bit_rate_Chosen == False):
            bit_rate = 0
        
        return bit_rate

    def TargetBuffer_index(self, buffer_size):

        if (buffer_size >= 0.4):
            if (buffer_size < 0.55):
                target_index = 1
            else:
                target_index = 0
        else:
            target_index = 0
            
        return target_index

    def Frame_Dropping_Control(self,next_quality,Delays):
    
        frame_time_len = 0.04
        Lambda = 5
        LANTENCY_PENALTY = 0.005
        SKIP_PENALTY = 0.5
        
        if Delays[-1] <= 1.0:
            LANTENCY_PENALTY = 0.005
        else:
            LANTENCY_PENALTY = 0.01
        
        next_latency_limit =  frame_time_len * (BIT_RATE[next_quality]/1000.0 + SKIP_PENALTY) / (LANTENCY_PENALTY*Lambda)
        return next_latency_limit

    # Define your algo
     # |   params           | params description                       |  example   |
     # | ------------------ | ---------------------------------------- | ---------- |
     # | time(s)            | physical time                            |   0.46(s)  |
     # | time_interval(s)   | duration in this cycle                   |   0.012(s) |  
     # | send_data_size(bit)| The data size downloaded in this cycle   |   14871(b) |
     # | frame_time_len(s)  | The time length of the frame currently   |   0.04(s)  |
     # | rebuf(s)           | The rebuf time of this cycle             |   0.00(s)  |
     # | buffer_size(s)     | The buffer size time length              |   1.26(s)  |
     # | play_time_len(s)   | The time length of playing in this cycle |   0.012(s) |
     # | end_delay(s)       | Current end-to-to delay                  |   1.31(s)  |
     # | cdn_newest_id      | Cdn the newest frame id                  |   85       |
     # | download_id        | Download frame id                        |   41       |
     # | cdn_has_frame      | cdn cumulative frame info                |   1.31(s)  |
     # | decision_flag      | Gop boundary flag or I frame flag        |   False    |
     # | buffer_flag        | Whether the player is buffering          |   False    |
     # | cdn_rebuf_flag     | Whether the cdn is rebuf                 |   False    |
     # | end_of_video       | Whether the end of video                 |   False    |
    def run(self, time, S_time_interval, S_send_data_size, S_chunk_len, S_rebuf, S_buffer_size, S_play_time_len,S_end_delay, S_decision_flag, S_buffer_flag,S_cdn_flag,S_skip_time, end_of_video, cdn_newest_id,download_id,cdn_has_frame,IntialVars):
        
        ##Search TargetBuffer Index
        target_buffer = self.TargetBuffer_index(S_buffer_size[-1])
        
        ##Search BitRate Index
        bit_rate = self.calculate_bitrate_index(S_send_data_size, S_time_interval, S_buffer_size)
        self.last_bitrate = bit_rate
        
        ##Search latency_limit
        latency_limit = self.Frame_Dropping_Control(next_quality = bit_rate, Delays = S_end_delay)
        
        ##judge special condition
        if (end_of_video == True):
            bit_rate = 0

        return bit_rate, target_buffer, latency_limit

    def get_params(self):
    # get your params
        your_params = [self.last_bitrate]
        return your_params

