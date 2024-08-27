import streamlit as st


st.set_page_config(layout="wide")

# Predefined code blocks with titles and code content
code_blocks = [
    {
        "title": "ex1.c - fork() and pipe()",
        "code": '''
#include<stdio.h>
#include<unistd.h>
#include<string.h>

int main(){
	char write_msg[] = "Hello child process";
	char read_msg[100];
	pid_t pid;
	int pipefd[2];
	
	if(pipe(pipefd)==-1){
		printf("error: pipe creation failed");
	}	
	pid = fork();
	if(pid<0){
		printf("error: child process creation failed");
	}
	else if(pid>0){
		close(pipefd[0]);
		write(pipefd[1],write_msg,strlen(write_msg));
		close(pipefd[1]);
		wait(NULL);
	}
	else{
		close(pipefd[1]);
		read(pipefd[0],read_msg,sizeof(read_msg));
		close(pipefd[0]);
		printf("The child has received %s",read_msg);
	}
	return 0;
}

'''
    },
    {
        "title": "ex1.c - bi-comunication",
        "code": '''
#include<stdio.h>
#include<unistd.h>
#include<string.h>

int main(){
	char p_to_c[] = "hi child, from parent";
	char p_buff[100];
	char c_buff[100];
	char c_to_p[] = "hi parent, from child";
	pid_t pid;
	int pipe_cp[2];
	int pipe_pc[2];
	
	if(pipe(pipe_cp)==-1 || pipe(pipe_pc)==-1){
		printf("Error: pipe creation has failed");
	}
	
	pid = fork();
	
	if(pid<0){
		printf("Error: child creation has failed");
	}
	else if(pid>0){
		close(pipe_pc[0]);
		close(pipe_cp[1]);
		write(pipe_pc[1],p_to_c,strlen(p_to_c)+1);
		printf("parent has sent the message\n");
		read(pipe_cp[0],p_buff,sizeof(p_buff));
		printf("parent read: %s \n",p_buff);
		close(pipe_pc[1]);
		close(pipe_cp[0]);
		wait(NULL);
	}
	else{
		close(pipe_pc[1]);
		close(pipe_cp[0]);
		write(pipe_cp[1],c_to_p,strlen(c_to_p)+1);
		printf("child has sent the message\n");
		read(pipe_pc[0],c_buff,sizeof(c_buff));
		printf("child read: %s \n",c_buff);
		close(pipe_pc[0]);
		close(pipe_cp[1]);
	}
	return 0;
}
'''
    },
    {
        "title": "ex2a.c - shared memory",
        "code": '''
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/ipc.h>
#include<sys/shm.h>

#define SHM_SIZE 1024
#define SHM_KEY 1234

int main(){
	key_t key = SHM_KEY;
	int shmid = shmget(key,SHM_SIZE,0666|IPC_CREAT);
	if(shmid==-1){
		printf("Error: Shared Mem. creation");
		exit(1);
	}
	
	pid_t pid = fork();
	if(pid<0){
		printf("Error: Child process creation");
		exit(1);
	}
	else if(pid>0){
		char *msg = "Hello from parent";
		char *shmptr = (char*)shmat(shmid,NULL,0);
		if(shmptr==(char*)-1){
			printf("Error: shm attach in parent");
			exit(1);
		}
		strncpy(shmptr,msg,SHM_SIZE);
		shmdt(shmptr);
		wait(NULL);
		shmctl(shmid,IPC_RMID,NULL);
	}
	else{
		char *shmptr = (char*)shmat(shmid,NULL,0);
		if(shmptr==(char*)-1){
			printf("Error: shm attach in child");
			exit(1);
		}
		printf("child received: %s",shmptr);
		shmdt(shmptr);
	}
	return 0;
}
'''
    },
    {
        "title": "ex2b.c - message passing",
        "code": '''
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<sys/ipc.h>
#include<sys/msg.h>

#define MSG_SIZE 256
#define MSG_KEY 1234

struct msgbuf{
	long mtype;
	char mtext[MSG_SIZE];
};

int main(){
	struct msgbuf message;
	key_t key = MSG_KEY;
	int msgid = msgget(key,IPC_CREAT|0666);
	if(msgid<0){
		printf("Error:");
		exit(1);
	}
	pid_t pid = fork();
	if(pid<0){
		printf("Error:");
		exit(1);
	}
	else if(pid>0){
		message.mtype = 1;
		printf("Enter the msg: ");
		fgets(message.mtext,MSG_SIZE,stdin);
		if(msgsnd(msgid,&message,strlen(message.mtext)+1,0)<0){
			printf("Error: ");
			exit(1);
		}
		wait(NULL);
		msgctl(msgid,IPC_RMID,NULL);
	}
	else{
		if(msgrcv(msgid,&message,MSG_SIZE,1,0)<0){
			printf("Error: ");
			exit(1);
		}
		printf("%s",message.mtext);
		_exit(0);
	}
	return 0;
}
'''
    },
    {
        "title": "ex3a.c - FCFS",
        "code": '''
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int arrival_time;
    int burst_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
} Process;

void FCFS(Process *process, int n) {
    int time = 0;
    for (int i = 0; i < n; i++) {
        if (time < process[i].arrival_time) {
            time = process[i].arrival_time;
        }
        process[i].completion_time = time + process[i].burst_time;
        process[i].turnaround_time = process[i].completion_time - process[i].arrival_time;
        process[i].waiting_time = process[i].turnaround_time - process[i].burst_time;
        time = process[i].completion_time;
    }
}

void printFCFS(Process *process, int n) {
    printf("Arrival time\tBurst time\tCompletion time\tTurnaround time\tWaiting time\n");
    int sum_wt = 0;
    int sum_tt = 0;
    for (int i = 0; i < n; i++) {
        printf("%d\t\t%d\t\t%d\t\t%d\t\t%d\n", 
            process[i].arrival_time, process[i].burst_time, 
            process[i].completion_time, process[i].turnaround_time, 
            process[i].waiting_time);
        sum_wt += process[i].waiting_time;
        sum_tt += process[i].turnaround_time;
    }
    printf("Average waiting time: %.2f\n", (float)sum_wt / n);
    printf("Average turnaround time: %.2f\n", (float)sum_tt / n);
}

void printGanttChart(Process *process, int n) {
    printf("\nGantt Chart:\n");

    for (int i = 0; i < n; i++) {
        printf("----");
    }
    printf("-\n");

    for (int i = 0; i < n; i++) {
        printf("| P%d ", i + 1);
    }
    printf("|\n");

    for (int i = 0; i < n; i++) {
        printf("----");
    }
    printf("-\n");

    printf("0");
    for (int i = 0; i < n; i++) {
        printf("   %d", process[i].completion_time);
    }
    printf("\n");
}

int main() {
    int n;
    printf("Enter the number of processes: ");
    scanf("%d", &n);
    Process *process = (Process *)malloc(n * sizeof(Process));
    for (int i = 0; i < n; i++) {
        printf("Enter arrival time and burst time for process %d: ", i + 1);
        scanf("%d %d", &process[i].arrival_time, &process[i].burst_time);
        process[i].completion_time = 0;
        process[i].turnaround_time = 0;
        process[i].waiting_time = 0;
    }

    FCFS(process, n);
    printFCFS(process, n);
    printGanttChart(process, n);

    free(process);
    return 0;
}


}
'''
    },
    {
        "title": "ex3a.c - Feedback",
        "code": '''
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define TQ_Q1 2 // Time quantum for Queue 1
#define TQ_Q2 4 // Time quantum for Queue 2

typedef struct {
    int arrival_time;
    int burst_time;
    int remaining_time;
    int completion_time;
    int waiting_time;
    int turnaround_time;
    int start_time;
} Process;

void feedback_queue(Process processes[], int n) {
    int time = 0, completed = 0;
    bool in_queue1[n], in_queue2[n];

    for (int i = 0; i < n; i++) {
        in_queue1[i] = in_queue2[i] = false;
        processes[i].remaining_time = processes[i].burst_time;
        processes[i].start_time = -1; 
    }

    while (completed < n) {
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= time && !in_queue1[i] && !in_queue2[i]) {
                in_queue1[i] = true;
            }
        }
        for (int i = 0; i < n; i++) {
            if (in_queue1[i]) {
                if (processes[i].start_time == -1) {
                    processes[i].start_time = time;
                }
                int tq = processes[i].remaining_time > TQ_Q1 ? TQ_Q1 : processes[i].remaining_time;
                time += tq;
                processes[i].remaining_time -= tq;
                if (processes[i].remaining_time == 0) {
                    processes[i].completion_time = time;
                    processes[i].turnaround_time = processes[i].completion_time - processes[i].arrival_time;
                    processes[i].waiting_time = processes[i].turnaround_time - processes[i].burst_time;
                    completed++;
                    in_queue1[i] = false;
                } else {
                    in_queue1[i] = false;
                    in_queue2[i] = true;
                }
            }
        }

        // Process Queue 2
        for (int i = 0; i < n; i++) {
            if (in_queue2[i]) {
                if (processes[i].start_time == -1) {
                    processes[i].start_time = time;
                }
                int tq = processes[i].remaining_time > TQ_Q2 ? TQ_Q2 : processes[i].remaining_time;
                time += tq;
                processes[i].remaining_time -= tq;
                if (processes[i].remaining_time == 0) {
                    processes[i].completion_time = time;
                    processes[i].turnaround_time = processes[i].completion_time - processes[i].arrival_time;
                    processes[i].waiting_time = processes[i].turnaround_time - processes[i].burst_time;
                    completed++;
                    in_queue2[i] = false;
                }
            }
        }
    }
}

void print_feedback_queue(Process processes[], int n) {
    int total_waiting_time = 0;
    int total_turnaround_time = 0;

    printf("Feedback Queue Scheduling:\n");
    printf("Process\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\n");
    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t\t%d\t\t%d\n", i+1, processes[i].arrival_time,
               processes[i].burst_time,
               processes[i].completion_time, processes[i].turnaround_time,
               processes[i].waiting_time);
        total_waiting_time += processes[i].waiting_time;
        total_turnaround_time += processes[i].turnaround_time;
    }

    printf("Average Waiting Time: %.2f\n", (float)total_waiting_time / n);
    printf("Average Turnaround Time: %.2f\n", (float)total_turnaround_time / n);
}

void print_gantt_chart(Process processes[], int n) {
    int time = 0;
    int max_time = 0;
    
    for (int i = 0; i < n; i++) {
        if (processes[i].completion_time > max_time) {
            max_time = processes[i].completion_time;
        }
    }

    printf("\nGantt Chart:\n");

    for (int i = 0; i < max_time; i++) {
        printf("--");
    }
    printf("-\n");

    for (int i = 0; i < max_time; i++) {
        int j;
        for (j = 0; j < n; j++) {
            if (processes[j].arrival_time <= i && processes[j].completion_time > i) {
                printf("| P%d ", j + 1);
                break;
            }
        }
        if (j == n) {
            printf("|    ");
        }
    }
    printf("|\n");

    for (int i = 0; i < max_time; i++) {
        printf("--");
    }
    printf("-\n");

    printf("0");
    for (int i = 1; i <= max_time; i++) {
        if (i % 2 == 0) {
            printf("   %d", i);
        }
    }
    printf("\n");
}

int main() {
    int n;

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    Process *processes = (Process *)malloc(n * sizeof(Process));
    if (processes == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        printf("Enter arrival time and burst time for process %d: ", i + 1);
        scanf("%d %d", &processes[i].arrival_time, &processes[i].burst_time);
        processes[i].completion_time = 0;
        processes[i].waiting_time = 0;
        processes[i].turnaround_time = 0;
    }

    feedback_queue(processes, n);
    print_feedback_queue(processes, n);
    print_gantt_chart(processes, n);

    free(processes);
    return 0;
}




}
'''
    },
    {
        "title": "ex3a.c - RR",
        "code": '''
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int arrival_time;
    int burst_time;
    int completion_time;
    int waiting_time;
    int turnaround_time;
} Process;

void round_robin(Process processes[], int n, int tq) {
    int remaining_burst[n];
    int time = 0;
    int completed = 0;
    int gantt_time[100], gantt_process[100]; // Arrays to store Gantt chart info
    int gantt_index = 0; // Gantt chart index

    for (int i = 0; i < n; i++) {
        remaining_burst[i] = processes[i].burst_time;
    }

    while (completed < n) {
        for (int i = 0; i < n; i++) {
            if (remaining_burst[i] > 0) {
                if (remaining_burst[i] <= tq) {
                    time += remaining_burst[i];
                    gantt_time[gantt_index] = time;  // Add time to Gantt chart
                    gantt_process[gantt_index] = i + 1;  // Add process to Gantt chart
                    gantt_index++;
                    processes[i].completion_time = time;
                    processes[i].turnaround_time = processes[i].completion_time - processes[i].arrival_time;
                    processes[i].waiting_time = processes[i].turnaround_time - processes[i].burst_time;
                    remaining_burst[i] = 0;
                    completed++;
                } else {
                    remaining_burst[i] -= tq;
                    time += tq;
                    gantt_time[gantt_index] = time;  // Add time to Gantt chart
                    gantt_process[gantt_index] = i + 1;  // Add process to Gantt chart
                    gantt_index++;
                }
            }
        }
    }

    // Print Gantt Chart
    printf("\nGantt Chart:\n");
    for (int i = 0; i < gantt_index; i++) {
        printf("----");
    }
    printf("-\n");

    for (int i = 0; i < gantt_index; i++) {
        printf("| P%d ", gantt_process[i]);
    }
    printf("|\n");

    for (int i = 0; i < gantt_index; i++) {
        printf("----");
    }
    printf("-\n");

    printf("0");
    for (int i = 0; i < gantt_index; i++) {
        printf("   %d", gantt_time[i]);
    }
    printf("\n");
}

void print_rr(Process processes[], int n) {
    int total_waiting_time = 0;
    int total_turnaround_time = 0;

    printf("RR Scheduling:\n");
    printf("Process\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\n");

    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t\t%d\t\t%d\n", i + 1, processes[i].arrival_time,
               processes[i].burst_time,
               processes[i].completion_time, processes[i].turnaround_time,
               processes[i].waiting_time);
        total_waiting_time += processes[i].waiting_time;
        total_turnaround_time += processes[i].turnaround_time;
    }

    printf("Average Waiting Time: %.2f\n", (float)total_waiting_time / n);
    printf("Average Turnaround Time: %.2f\n", (float)total_turnaround_time / n);
}

int main() {
    int n, tq;

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    printf("Enter the time quantum: ");
    scanf("%d", &tq);

    Process *processes = (Process *)malloc(n * sizeof(Process));
    if (processes == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        printf("Enter arrival time and burst time for process %d: ", i + 1);
        scanf("%d %d", &processes[i].arrival_time, &processes[i].burst_time);
        processes[i].completion_time = 0;
        processes[i].waiting_time = 0;
        processes[i].turnaround_time = 0;
    }

    round_robin(processes, n, tq);
    print_rr(processes, n);
    free(processes);

    return 0;
}


'''
    },
    {
        "title": "ex3a.c - SJF",
        "code": '''
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int arrival_time;
    int burst_time;
    int completion_time;
    int waiting_time;
    int turnaround_time;
    int process_id;
} Process;

void sjf(Process processes[], int n) {
    int time = 0;
    int completed = 0;
    int min_index;
    int min_burst;

    while (completed < n) {
        min_burst = 10000;
        min_index = -1;

        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= time &&
                processes[i].completion_time == 0 &&
                processes[i].burst_time < min_burst) {
                min_burst = processes[i].burst_time;
                min_index = i;
            }
        }

        if (min_index != -1) {
            time += processes[min_index].burst_time;
            processes[min_index].completion_time = time;
            processes[min_index].turnaround_time = processes[min_index].completion_time - processes[min_index].arrival_time;
            processes[min_index].waiting_time = processes[min_index].turnaround_time - processes[min_index].burst_time;
            completed++;
        } else {
            time++;
        }
    }
}

void print_gantt_chart(Process processes[], int n) {
    printf("\nGantt Chart:\n");

    // Sort processes by completion time to reflect the correct execution order
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (processes[j].completion_time > processes[j + 1].completion_time) {
                Process temp = processes[j];
                processes[j] = processes[j + 1];
                processes[j + 1] = temp;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        printf("----");
    }
    printf("-\n");

    for (int i = 0; i < n; i++) {
        printf("| P%d ", processes[i].process_id);
    }
    printf("|\n");

    for (int i = 0; i < n; i++) {
        printf("----");
    }
    printf("-\n");

    printf("0");
    for (int i = 0; i < n; i++) {
        printf("   %d", processes[i].completion_time);
    }
    printf("\n");
}

void print_sjf(Process processes[], int n) {
    int total_waiting_time = 0;
    int total_turnaround_time = 0;

    printf("SJF Scheduling:\n");
    printf("Process\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\n");

    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t\t%d\t\t%d\n", processes[i].process_id, 
               processes[i].arrival_time,
               processes[i].burst_time,
               processes[i].completion_time, processes[i].turnaround_time,
               processes[i].waiting_time);
        total_waiting_time += processes[i].waiting_time;
        total_turnaround_time += processes[i].turnaround_time;
    }

    printf("Average Waiting Time: %.2f\n", (float)total_waiting_time / n);
    printf("Average Turnaround Time: %.2f\n", (float)total_turnaround_time / n);
}

int main() {
    int n;
    printf("Enter the number of processes: ");
    scanf("%d", &n);

    Process *processes = (Process *)malloc(n * sizeof(Process));
    if (processes == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        processes[i].process_id = i + 1;
        printf("Enter arrival time and burst time for process %d: ", i + 1);
        scanf("%d %d", &processes[i].arrival_time, &processes[i].burst_time);
        processes[i].completion_time = 0;
        processes[i].waiting_time = 0;
        processes[i].turnaround_time = 0;
    }

    sjf(processes, n);
    print_sjf(processes, n);
    print_gantt_chart(processes, n);

    free(processes);

    return 0;
}





}
'''
    },
    {
        "title": "ex3a.c - SJF",
        "code": '''
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int arrival_time;
    int burst_time;
    int completion_time;
    int waiting_time;
    int turnaround_time;
} Process;

void srt(Process processes[], int n) {
    int remaining_burst[n];
    int time = 0;
    int completed = 0;
    int min_index;

    for (int i = 0; i < n; i++) {
        remaining_burst[i] = processes[i].burst_time;
    }

    while (completed < n) {
        min_index = -1;
        int min_remaining = 10000;

        for (int i = 0; i < n; i++) {
            if (processes[i].arrival_time <= time && remaining_burst[i] > 0 &&
                remaining_burst[i] < min_remaining) {
                min_remaining = remaining_burst[i];
                min_index = i;
            }
        }

        if (min_index != -1) {
            remaining_burst[min_index]--;
            time++;
            if (remaining_burst[min_index] == 0) {
                processes[min_index].completion_time = time;
                processes[min_index].turnaround_time = processes[min_index].completion_time -
                    processes[min_index].arrival_time;
                processes[min_index].waiting_time = processes[min_index].turnaround_time -
                    processes[min_index].burst_time;
                completed++;
            }
        } else {
            time++;
        }
    }
}

void print_srt(Process processes[], int n) {
    int total_waiting_time = 0;
    int total_turnaround_time = 0;

    printf("SRT Scheduling:\n");
    printf("Process\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\n");

    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t\t%d\t\t%d\n", i + 1, processes[i].arrival_time,
            processes[i].burst_time,
            processes[i].completion_time, processes[i].turnaround_time,
            processes[i].waiting_time);
        total_waiting_time += processes[i].waiting_time;
        total_turnaround_time += processes[i].turnaround_time;
    }

    printf("Average Waiting Time: %.2f\n", (float)total_waiting_time / n);
    printf("Average Turnaround Time: %.2f\n", (float)total_turnaround_time / n);
}

void print_gantt_chart(Process processes[], int n) {
    int max_time = 0;
    for (int i = 0; i < n; i++) {
        if (processes[i].completion_time > max_time) {
            max_time = processes[i].completion_time;
        }
    }

    printf("\nGantt Chart:\n");

    for (int i = 0; i < max_time; i++) {
        printf("--");
    }
    printf("-\n");

    for (int i = 0; i < n; i++) {
        printf("| P%d ", i + 1);
    }
    printf("|\n");

    for (int i = 0; i < max_time; i++) {
        printf("--");
    }
    printf("-\n");

    printf("0");
    for (int i = 0; i < n; i++) {
        printf("   %d", processes[i].completion_time);
    }
    printf("\n");
}

int main() {
    int n;

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    Process *processes = (Process *)malloc(n * sizeof(Process));
    if (processes == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        printf("Enter arrival time and burst time for process %d: ", i + 1);
        scanf("%d %d", &processes[i].arrival_time, &processes[i].burst_time);
        processes[i].completion_time = 0;
        processes[i].waiting_time = 0;
        processes[i].turnaround_time = 0;
    }

    srt(processes, n);
    print_srt(processes, n);
    print_gantt_chart(processes, n);

    free(processes);
    return 0;
}



}
'''
    },
    {
        "title": "ex3b.c - CPU sched.",
        "code": '''
#include <stdio.h>

typedef struct {
    int arrival_time;
    int cpu1_burst_time;
    int io_burst_time;
    int cpu2_burst_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
} Process;

void fcfs_with_io(Process processes[], int n) {
    int time = 0;

    for (int i = 0; i < n; i++) {
        if (time < processes[i].arrival_time) {
            time = processes[i].arrival_time;
        }
        printf("P%d (CPU1: %d ms to %d ms), goes for I/O\n", i + 1, time, time + processes[i].cpu1_burst_time);
        time += processes[i].cpu1_burst_time;
        time += processes[i].io_burst_time;
        printf("P%d (CPU2: %d ms to %d ms), completes\n", i + 1, time, time + processes[i].cpu2_burst_time);
        time += processes[i].cpu2_burst_time;
        processes[i].completion_time = time;
        processes[i].turnaround_time = processes[i].completion_time - processes[i].arrival_time;
        processes[i].waiting_time = processes[i].turnaround_time - (processes[i].cpu1_burst_time + processes[i].cpu2_burst_time);
    }
}

void print_processes(Process processes[], int n) {
    int total_wt = 0, total_tt = 0;
    
    printf("Process\tArrival\tCPU1\tI/O\tCPU2\tCompletion\tTurnaround\tWaiting\n");
    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t%d\t%d\t\t%d\t\t%d\n", i + 1, processes[i].arrival_time,
               processes[i].cpu1_burst_time, processes[i].io_burst_time,
               processes[i].cpu2_burst_time, processes[i].completion_time,
               processes[i].turnaround_time, processes[i].waiting_time);
        total_wt += processes[i].waiting_time;
        total_tt += processes[i].turnaround_time;
    }

    printf("Average Waiting Time: %.2f\n", (float)total_wt / n);
    printf("Average Turnaround Time: %.2f\n", (float)total_tt / n);
}

int main() {
    int n;

    printf("Enter number of processes: ");
    scanf("%d", &n);

    Process processes[n];

    for (int i = 0; i < n; i++) {
        printf("Enter arrival time, CPU1 burst time, I/O burst time, CPU2 burst time for P%d:\n", i + 1);
        scanf("%d %d %d %d", &processes[i].arrival_time, &processes[i].cpu1_burst_time,
              &processes[i].io_burst_time, &processes[i].cpu2_burst_time);
    }

    fcfs_with_io(processes, n);
    print_processes(processes, n);

    return 0;
}




'''
    },
    {
        "title": "ex4.c - Thread",
        "code": '''
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_THREADS 10 // Define a maximum number of threads for simplicity

typedef struct {
    int thread_id;
    int sleep_duration;
} ThreadData;

// Function prototype
void* thread_function(void* arg);

int main() {
    pthread_t threads[MAX_THREADS];
    pthread_attr_t attr;
    struct sched_param param;
    ThreadData thread_data[MAX_THREADS];
    int num_threads;
    int ret;

    // Prompt user for the number of threads
    printf("Enter the number of threads (max %d): ", MAX_THREADS);
    if (scanf("%d", &num_threads) != 1 || num_threads > MAX_THREADS || num_threads <= 0) {
        fprintf(stderr, "Invalid number of threads. Exiting.\n");
        return EXIT_FAILURE;
    }

    // Prompt user for sleep durations
    for (int i = 0; i < num_threads; i++) {
        printf("Enter sleep duration for thread %d (in seconds): ", i + 1);
        if (scanf("%d", &thread_data[i].sleep_duration) != 1 || thread_data[i].sleep_duration < 0) {
            fprintf(stderr, "Invalid sleep duration. Exiting.\n");
            return EXIT_FAILURE;
        }
        thread_data[i].thread_id = i + 1;
    }

    // Initialize thread attributes
    pthread_attr_init(&attr);
    
    // Set thread attributes to use the highest priority
    if (pthread_attr_setschedpolicy(&attr, SCHED_FIFO) != 0) {
        fprintf(stderr, "Error setting scheduling policy.\n");
        return EXIT_FAILURE;
    }
    param.sched_priority = 10; // Highest priority
    if (pthread_attr_setschedparam(&attr, &param) != 0) {
        fprintf(stderr, "Error setting scheduling parameters.\n");
        return EXIT_FAILURE;
    }

    // Create threads with user-specified parameters
    for (int i = 0; i < num_threads; i++) {
        ret = pthread_create(&threads[i], &attr, thread_function, &thread_data[i]);
        if (ret) {
            fprintf(stderr, "Error creating thread %d: %s\n", i + 1, strerror(ret));
            exit(EXIT_FAILURE);
        }
    }

    // Wait for all threads to complete
    for (int i = 0; i < num_threads; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            fprintf(stderr, "Error joining thread %d.\n", i + 1);
            exit(EXIT_FAILURE);
        }
    }

    // Destroy thread attributes
    pthread_attr_destroy(&attr);

    return 0;
}

void* thread_function(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    printf("Thread %d is running\n", data->thread_id);
    sleep(data->sleep_duration); // Simulate work
    printf("Thread %d is finished\n", data->thread_id);
    return NULL;
}
}
'''
    },
    
]

# Search bar to filter code blocks
search_query = st.text_input("Search Code Blocks", "").lower()

# Filter code blocks based on search query
filtered_code_blocks = [block for block in code_blocks if search_query in block["title"].lower()]

# Display filtered code blocks in a horizontal layout
st.title("Stored Codes")

if filtered_code_blocks:
    cols = st.columns(len(filtered_code_blocks))
    for i, block in enumerate(filtered_code_blocks):
        with cols[i]:
            with st.expander(block["title"]):
                st.code(block["code"], language="python" if "python" in block["title"].lower() else "html")
else:
    st.write("No code blocks found.")
