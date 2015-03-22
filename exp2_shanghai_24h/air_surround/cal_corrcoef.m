function [] = cal_corrcoef( )
%CAL_CORRCOEF Summary of this function goes here
%   Detailed explanation goes here
data = load('city_history2.txt');
[N,M] = size(data);
shanghai_data = data(:,2);
other_data = data(:,3:end);
shanghai_data = shanghai_data(7:N,:);
other_data = other_data(1:N-6,:);

for i=1:(M-2)
    tmp = corrcoef(shanghai_data,other_data(:,i));
    fprintf('%d: %f\n',i,tmp(1,2));
    %corrcoef(shanghai_data,other_data(:,i))
end
end

