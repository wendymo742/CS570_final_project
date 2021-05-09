
* Import the 15% sample dataset of biweekly time series of days under medication;
proc import datafile="C:\Users\yche465\Desktop\CS570\Project\DrugDay15.csv" out=drugday15;
run;

*Convert to biweekly time series of PDC (length = 52 biweekly intervals);
data PDC;
set drugday15;
ID = _N_;
array a{52} column1-column52;
array b{52} PDC1-PDC52;
array c{52} T1-T52;
do i=1 to 52;
	b{i}=a{i}/14;
	c{i}=i;
	end;
rename Var1=Ref_ID;
keep Var1 ID PDC1-PDC52 T1-T52;
run;

*Create a macro function for implementing the GBTM procedures (under censored normal distribution) at a pre-specified k value;
%macro Traj(dataset,k);
	*create macro variable for the order parameter;
	data seq;
	do i=1 to &k;
	order=3;
	output;
	end;
	run;

	proc sql noprint;
	select order
	into :orderlist separated by ' '
	from seq; 
	quit;
	
	*Run the finite mixture trajectory model under censored normal distribution;
	PROC TRAJ DATA=&dataset OUTPLOT=OP OUTSTAT=OS OUT=OF OUTEST=OE ITDETAIL;
	    ID ID; VAR PDC1-PDC52; INDEP T1-T52;
	    MODEL CNORM; MIN 0;MAX 1; NGROUPS &k; ORDER &orderlist;
	RUN;
	*output model fitness metrics;
	data modelfit&k;
	retain K _LOGLIK_ _BIC1_ _AIC_;
	set oe;
	K=&k;
	where _TYPE_="PARMS";
	rename _LOGLIK_=LN_LIK _BIC1_=BIC _AIC_=AIC;  
	keep K _LOGLIK_ _BIC1_ _AIC_; 
	run;
%mend;

*Create a macro function to iteratively implement GBTM fitting across various k values and output fit statistics;
%macro rep_traj(data,maxk);
%DO I = 2 %TO &maxk;
 %Traj(&data,&I);
%END;

data modfit;
do i=2 to &maxk;
datname=cat("modelfit",i);
output;
end;
run;

proc sql noprint;
select datname
into :datname separated by ' '
from modfit; 
quit;

data fit;
set &datname;
run;
%mend rep_traj;


*Conduct GBTM fitting for k=2~10; 
%rep_traj(PDC,10)


*We determine that k=7 results in the optimal balance between fitness test statistics and interpretable number of clusters ;
PROC TRAJ DATA=PDC OUTPLOT=OP OUTSTAT=OS OUT=OF OUTEST=OE ITDETAIL;
ID ID; VAR PDC1-PDC52; INDEP T1-T52;
MODEL CNORM; MIN 0;MAX 1; NGROUPS 7; ORDER 3 3 3 3 3 3 3;
RUN;


*Export the k=7 model predictions and weighted averages by follow-up time to a csv file;
proc export data=OP
    outfile="C:\Users\yche465\Desktop\CS570\Project\AvgPred.csv"
    dbms=csv;
run;

*Export the k=7 model parameters' estimates to a csv file;
proc export data=OS
    outfile="C:\Users\yche465\Desktop\CS570\Project\Est_Pct.csv"
    dbms=csv;
run;
