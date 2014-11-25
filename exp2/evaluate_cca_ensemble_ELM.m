function evaluate_cca_ensemble_ELM( station )
%EVALUATE_CCA_ENSEMBLE_ELM Summary of this function goes here
%   Detailed explanation goes here

station = 'beijing';
version = '1';
type1 = 'increase';
type2 = 'low';

ROUND_NUM = 4;
REPEAT_NUM = 10;
LIMIT_OF_EMPTY = 6;

d = loadData(station, version, type1, type2);
d = extract_record(d,LIMIT_OF_EMPTY);
d = equalize_label(d);
d = d(randperm(length(d)),:); 
d = myNormalize(d);  
        
Test_Accuracy = 0; 
for k = 1:REPEAT_NUM
    for i = 1:ROUND_NUM
%%%%% air + mete + air_surround + mete_surround
        [Tr,Te] = dataPartion(d,i,ROUND_NUM);
        T1 = my_predict(Tr(:,1), Tr(:,2:7), Tr(:,8:14), Te(:,1), Te(:,2:7), Te(:,8:14)); 
        T2 = my_predict(Tr(:,1), Tr(:,2:7), Tr(:,15:19), Te(:,1), Te(:,2:7), Te(:,15:19));
        T3 = my_predict(Tr(:,1), Tr(:,2:7), Tr(:,20:54), Te(:,1), Te(:,2:7), Te(:,20:54));
        T4 = my_predict(Tr(:,1), Tr(:,8:14), Tr(:,15:19), Te(:,1), Te(:,8:14), Te(:,15:19));
        [T5,T_Expected] = my_predict(Tr(:,1), Tr(:,15:19), Tr(:,20:54), Te(:,1), Te(:,15:19), Te(:,20:54));
        T_Actual = (T1 + T2 + T3 + T4 + T5)/5;

%%%%% air  + mete + air surround
%        T1 = my_predict(Tr(:,1), Tr(:,2:7), Tr(:,8:14), Te(:,1), Te(:,2:7), Te(:,8:14)); 
%        T2 = my_predict(Tr(:,1), Tr(:,2:7), Tr(:,15:19), Te(:,1), Te(:,2:7), Te(:,15:19));
%        [T4 ,T_Expected] = my_predict(Tr(:,1), Tr(:,8:14), Tr(:,15:19), Te(:,1), Te(:,8:14), Te(:,15:19));
%        T_Actual = (T1 + T2 + T4)/3;
        
        num = 0;
        for j = 1:size(T_Actual,1)
            [x,label_Actual] = max(T_Actual(j,:));
            [x,label_Expected] = max(T_Expected(j,:));
            if label_Actual == label_Expected
                num = num + 1;
            end
        end
        Test_Accuracy = Test_Accuracy + num/size(T_Actual,1);
    end
end

Test_Accuracy = Test_Accuracy/(REPEAT_NUM*ROUND_NUM);
fprintf('Test_Accuracy: %f \n',Test_Accuracy);
fprintf('Size of d: %d \n', size(d,1));
end

function [Te_Actual,Te_Expected] = my_predict(Tr_Labs,Tr_Atts1,Tr_Atts2,Te_Labs, Te_Atts1,Te_Atts2)
    CCA = 0;
    HIDDEN_NUM = 100;
    if CCA == 1
        [A,B,r,U,V] = canoncorr(Tr_Atts1,Tr_Atts2);
        Tr_Atts = [U V];
        N = size(Te_Atts1,1);
        Te_Atts = [(Te_Atts1-repmat(mean(Te_Atts1),N,1))*A (Te_Atts2-repmat(mean(Te_Atts2),N,1))*B];
        fprintf('Canonical correlation: %f\n',r);
    else
        Tr_Atts = [Tr_Atts1 Tr_Atts2];
        Te_Atts = [Te_Atts1 Te_Atts2];
    end
    [Te_Actual,Te_Expected] = my_ELM2(Tr_Labs,Tr_Atts, Te_Labs, Te_Atts, 1, HIDDEN_NUM, 'sig');

end

function [Tr, Te] = dataPartion(d,i,ROUND_NUM)
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
end

function [d] = loadData(station, version, type1, type2)
    
    air_range = 2:7;
    mete_range = 2:8;
    air_surround_range = 2:6;
    mete_surround_range = 2:36;
%    air_surround_diff_range = 2:6;
%    traffic_range = 2;
    air_f1 = ['air/' station '_' type1 version '.txt'];
    air_f0 = ['air/' station '_' type2 version '.txt'];
    mete_f1 = ['mete/' station '_' type1 version '.txt'];
    mete_f0 = ['mete/' station '_' type2 version '.txt'];
    air_surround_f1 = ['air_surround/' station '_' type1 version '.txt'];
    air_surround_f0 = ['air_surround/' station '_' type2 version '.txt'];
    mete_surround_f1 = ['mete_surround/' station '_' type1 version '.txt'];
    mete_surround_f0 = ['mete_surround/' station '_' type2 version '.txt'];
%    air_surround_diff_f1 = ['air_surround_diff/' station '_' type1 version '.txt'];
%    air_surround_diff_f0 = ['air_surround_diff/' station '_' type2 version '.txt'];
%    traffic_f1 = ['traffic/' station '_' type1 version '.txt'];
%    traffic_f0 = ['traffic/' station '_' type2 version '.txt'];

    tmp_d = load(air_f1);
    d1 = tmp_d(:,air_range);
    tmp_d = load(air_f0);
    d0 = tmp_d(:,air_range);
    
    tmp_d = load(mete_f1);
    d1 = [d1 tmp_d(:,mete_range)];
    tmp_d = load(mete_f0);
    d0 = [d0 tmp_d(:,mete_range)];
   
    tmp_d = load(air_surround_f1);
    d1 = [d1 tmp_d(:,air_surround_range)];
    tmp_d = load(air_surround_f0);
    d0 = [d0 tmp_d(:,air_surround_range)];
    
    tmp_d = load(mete_surround_f1);
    d1 = [d1 tmp_d(:,mete_surround_range)];
    tmp_d = load(mete_surround_f0);
    d0 = [d0 tmp_d(:,mete_surround_range)];
    
    d1 = [ones(size(d1,1),1) d1];
    d0 = [zeros(size(d0,1),1) d0];
    d = [d1;d0];
    
end

function [rd] = extract_record(d,limit)
    rd = [];
    M = size(d,1);
    for row = 1:M
       if(size(find(d(row,:)==-1),2)<=limit)
           rd = [rd;d(row,:)];
       end
    end
end

function [rd] = equalize_label(d)
    indexes1 = find(d(:,1)==1);
    num1 = length(indexes1);
    indexes0 = find(d(:,1)==0);
    indexes0 = indexes0(randperm(length(indexes0)));
    indexes0 = indexes0(1:num1);
    rd = d([indexes1;indexes0],:);
end

function [n_d] = myNormalize(d)
    for col = 2:size(d,2)
        ma = max(d(:,col));
        mi = min(d(:,col));
        d(:,col) = (d(:,col)-mi)/(ma-mi);
    end
    n_d = d;
end

