function [ output_args ] = evaluation_ELM_k( input_args )
%EVALUATION_ELM_K Summary of this function goes here
%   Detailed explanation goes here


for k = 1:length(Te)
       M = [];
       for j=1:LABEL_NUM:
            [P] = my_elm_predict(Te(k,3:8), strcat(num2str(j),'.mat'));
            M = [M',P']';
       end
       V = zeros(LABEL_NUM);
       V[Te(k,9)]=1;
       R = V * M;
       [x, label_index_actual]=max(R);   
       if label_index_actual == Te(k,10):
            right_num = right_num + 1;
       end
   end

end

