import sys
from collections import deque

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = -1
        self.waiting_time = 0
        self.response_time = -1
    
    def copy(self):
        """ایجاد یک کپی جدید از فرآیند"""
        new_process = Process(self.pid, self.arrival_time, self.burst_time)
        new_process.remaining_time = self.remaining_time
        new_process.start_time = self.start_time
        new_process.finish_time = self.finish_time
        new_process.waiting_time = self.waiting_time
        new_process.response_time = self.response_time
        return new_process

# ابتدا توابع الگوریتم‌ها را تعریف می‌کنیم
def fcfs(processes):
    time = 0
    for p in sorted(processes, key=lambda x: x.arrival_time):
        if time < p.arrival_time:
            time = p.arrival_time
        p.start_time = time
        p.finish_time = time + p.burst_time
        p.waiting_time = p.start_time - p.arrival_time
        p.response_time = p.start_time - p.arrival_time
        time = p.finish_time
    
    turnaround_times = [p.finish_time - p.arrival_time for p in processes]
    waiting_times = [p.waiting_time for p in processes]
    response_times = [p.response_time for p in processes]
    
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    avg_waiting = sum(waiting_times) / len(waiting_times)
    avg_response = sum(response_times) / len(response_times)
    
    return avg_turnaround, avg_waiting, avg_response

def sjf(processes):
    time = 0
    remaining_processes = processes.copy()
    completed_processes = []
    
    while remaining_processes:
        arrived = [p for p in remaining_processes if p.arrival_time <= time]
        if not arrived:
            time += 1
            continue
        
        shortest = min(arrived, key=lambda x: x.burst_time)
        remaining_processes.remove(shortest)
        
        shortest.start_time = time
        shortest.finish_time = time + shortest.burst_time
        shortest.waiting_time = shortest.start_time - shortest.arrival_time
        shortest.response_time = shortest.start_time - shortest.arrival_time
        time = shortest.finish_time
        completed_processes.append(shortest)
    
    turnaround_times = [p.finish_time - p.arrival_time for p in completed_processes]
    waiting_times = [p.waiting_time for p in completed_processes]
    response_times = [p.response_time for p in completed_processes]
    
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    avg_waiting = sum(waiting_times) / len(waiting_times)
    avg_response = sum(response_times) / len(response_times)
    
    return avg_turnaround, avg_waiting, avg_response

def rr(processes, quantum):
    time = 0
    queue = deque()
    remaining_processes = processes.copy()
    completed_processes = []
    
    while remaining_processes or queue:
        arrived = [p for p in remaining_processes if p.arrival_time <= time]
        for p in arrived:
            queue.append(p)
            remaining_processes.remove(p)
        
        if not queue:
            time += 1
            continue
        
        current = queue.popleft()
        
        if current.response_time == -1:
            current.response_time = time - current.arrival_time
        
        if current.remaining_time > quantum:
            time += quantum
            current.remaining_time -= quantum
            queue.append(current)
        else:
            time += current.remaining_time
            current.remaining_time = 0
            current.finish_time = time
            current.waiting_time = current.finish_time - current.arrival_time - current.burst_time
            completed_processes.append(current)
    
    turnaround_times = [p.finish_time - p.arrival_time for p in completed_processes]
    waiting_times = [p.waiting_time for p in completed_processes]
    response_times = [p.response_time for p in completed_processes]
    
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    avg_waiting = sum(waiting_times) / len(waiting_times)
    avg_response = sum(response_times) / len(response_times)
    
    return avg_turnaround, avg_waiting, avg_response

# حالا تابع تست را تعریف می‌کنیم
def test_case_1():
    processes = [
        Process(1, 0, 8),
        Process(2, 1, 4),
        Process(3, 2, 9)
    ]
    
    # FCFS
    fcfs_turnaround, fcfs_waiting, fcfs_response = fcfs([p.copy() for p in processes])
    print("==== Test Case 1 ====")
    print(f"FCFS: Calculated: Turnaround: {fcfs_turnaround:.2f}, Waiting: {fcfs_waiting:.2f}, Response: {fcfs_response:.2f}")
    print(f"      Expected:   Turnaround: 15.00, Waiting: 7.33, Response: 7.33")
    
    # SJF
    sjf_turnaround, sjf_waiting, sjf_response = sjf([p.copy() for p in processes])
    print(f"SJF:  Calculated: Turnaround: {sjf_turnaround:.2f}, Waiting: {sjf_waiting:.2f}, Response: {sjf_response:.2f}")
    print(f"      Expected:   Turnaround: 12.33, Waiting: 4.67, Response: 4.67")
    
    # RR with quantum=4
    rr_turnaround, rr_waiting, rr_response = rr([p.copy() for p in processes], 4)
    print(f"RR (Quantum = 4): Calculated: Turnaround: {rr_turnaround:.2f}, Waiting: {rr_waiting:.2f}, Response: {rr_response:.2f}")
    print(f"                  Expected:   Turnaround: 15.67, Waiting: 8.00, Response: 1.33")
    
    # Check if all passed
    fcfs_passed = abs(fcfs_turnaround - 15.00) < 0.01 and abs(fcfs_waiting - 7.33) < 0.01 and abs(fcfs_response - 7.33) < 0.01
    sjf_passed = abs(sjf_turnaround - 12.33) < 0.01 and abs(sjf_waiting - 4.67) < 0.01 and abs(sjf_response - 4.67) < 0.01
    rr_passed = abs(rr_turnaround - 15.67) < 0.01 and abs(rr_waiting - 8.00) < 0.01 and abs(rr_response - 1.33) < 0.01
    
    if fcfs_passed and sjf_passed and rr_passed:
        print(">>> Test Case 1 PASSED.")
    else:
        print(">>> Test Case 1 FAILED.")

if __name__ == "__main__":
    test_case_1()