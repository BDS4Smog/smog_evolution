function evaluate_ELM( range,station )
%EVALUATE_ELM Summary of this function goes here
%   Detailed explanation goes here
%Local air
station = 'beijing';
version = '2'

f1 = ['data/' station '_decrease.txt'];
f0 = ['data/' station '_high.txt'];
type1 = 'decrease'
type2 = 'high'

HIDDEN_NUM = 100;
ROUND_NUM = 4;
REPEAT_NUM =200;

LIMIT_OF_EMPTY = 0

field = [1 0 0 0 0]

%air_range = [2:7];
air_range = [2:7];
mete_range = [2:8];
air_surround_range = [2:6];
%mete_surround_range = [2:21];
mete_surround_range = [2:36];
air_surround_diff_range = [2:6]

air_f1 = ['air/' station '_' type1 version '.txt'];
air_f0 = ['air/' station '_' type2 version '.txt'];
mete_f1 = ['mete/' station '_' type1 version '.txt'];
mete_f0 = ['mete/' station '_' type2 version '.txt'];
air_surround_f1 = ['air_surround/' station '_' type1 version '.txt'];
air_surround_f0 = ['air_surround/' station '_' type2 version '.txt'];
mete_surround_f1 = ['mete_surround/' station '_' type1 version '.txt'];
mete_surround_f0 = ['mete_surround/' station '_' type2 version '.txt'];
air_surround_diff_f1 = ['air_surround_diff/' station '_' type1 version '.txt'];
air_surround_diff_f0 = ['air_surround_diff/' station '_' type2 version '.txt'];


d1 = []
d0 = []
if field(1)==1
    tmp_d = load(air_f1);
    d1 = [d1 tmp_d(:,air_range)]
    tmp_d = load(air_f0);
    d0 = [d0 tmp_d(:,air_range)]
end
if field(2)==1
    tmp_d = load(mete_f1);
    d1 = [d1 tmp_d(:,mete_range)]
    tmp_d = load(mete_f0);
    d0 = [d0 tmp_d(:,mete_range)]
end
if field(3)==1
    tmp_d = load(air_surround_f1);
    d1 = [d1 tmp_d(:,air_surround_range)]
    tmp_d = load(air_surround_f0);
    d0 = [d0 tmp_d(:,air_surround_range)]
end
if field(4)==1
    tmp_d = load(mete_surround_f1);
    d1 = [d1 tmp_d(:,mete_surround_range)]
    tmp_d = load(mete_surround_f0);
    d0 = [d0 tmp_d(:,mete_surround_range)]
end
if field(5)==1
    tmp_d = load(air_surround_diff_f1);
    d1 = [d1 tmp_d(:,air_surround_diff_range)]
    tmp_d = load(air_surround_diff_f0);
    d0 = [d0 tmp_d(:,air_surround_diff_range)]
end

%    tmp_d1 = [max((d1(:,[15 21 27 33]))')' min((d1(:,[15 21 27 33]))')'];
d1 = [ones(size(d1,1),1) d1];
%    d1 = compRecord(d1);
d1 = extract_record(d1,LIMIT_OF_EMPTY);
%    tmp_d0 = [max((d0(:,[15 21 27 33]))')' min((d0(:,[15 21 27 33]))')'];
d0 = [zeros(size(d0,1),1) d0];
%    d0 = compRecord(d0);
d0 = extract_record(d0,LIMIT_OF_EMPTY);
   
n_record = size(d1,1);
Train_Accuracy = 0;
Test_Accuracy = 0; 

for k = 1:REPEAT_NUM
    d0 = d0(randperm(length(d0)),:); 
    d0 = d0(1:size(d1,1),:);
%    d = [d0' d1']';
    d = [d0;d1];
    d = d(randperm(length(d)),:); 
    d = myNormalize(d);
    
    for i = 1:ROUND_NUM
        start_1 = 1+(i-1)*floor(length(d)/ROUND_NUM);
        end_1 = i*floor(length(d)/ROUND_NUM); 
        Te = d(start_1:end_1,:);
        if i == 1
            Tr = d(end_1+1:length(d),:);
        elseif i == ROUND_NUM
            Tr = d(1:start_1-1,:);
        else
            Tr = [d(1:start_1-1,:)',d(end_1+1:length(d),:)']';    
        end
        [Tr_acc, Te_acc] = my_ELM(Tr, Te, 1, HIDDEN_NUM, 'sig');
        Train_Accuracy = Train_Accuracy + Tr_acc;
        Test_Accuracy = Test_Accuracy + Te_acc;
    end
end
Train_Accuracy = Train_Accuracy/(ROUND_NUM*REPEAT_NUM);
Test_Accuracy = Test_Accuracy/(ROUND_NUM*REPEAT_NUM);
fprintf('Train_Accuracy: %f \n',Train_Accuracy);
fprintf('Test_Accuracy: %f \n',Test_Accuracy);
fprintf('Number of records: %d \n',n_record*2);

end

function [r_d] = compRecord(d)
    for col = 2:size(d,2)
        d = d(find(d(:,col)~=-1),:);
    end
    r_d = d;
end
function [rd] = extract_record(d,limit)
    rd = [];
    [M N]=size(d);
    for row = 1:M
       if(size(find(d(row,:)==-1),2)<=limit)
           rd = [rd;d(row,:)];
       end
    end
end

function [n_d] = myNormalize(d)
    for col = 2:size(d,2)
        ma = max(d(:,col));
        mi = min(d(:,col));
        d(:,col) = (d(:,col)-mi)/(ma-mi);
    end
    n_d = d;
end

