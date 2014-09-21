function [ output_args ] = test( input_args )
%SELECT_CITY Summary of this function goes here
%   Detailed explanation goes here
%n_dist = 10;
%n_aqi = 8;
n_dist = 10;
n_aqi = 8;

dist_dic = load('dist_matrix');
dist_bj = dist_dic(:,14);
[a,b] = sort(dist_bj);
cities = b(1:n_dist);

aqi_dic = load('aqi_gt_200');
aqi_bj = aqi_dic(cities);
[c,d] = sort(aqi_bj,1,'descend');
d = d(1:n_aqi);
final = cities(d);

fp=fopen('in.txt','w'); 
for i=1:n_aqi
    fprintf(fp,'%d\n',final(i));  
end

X = load('X_1');
y = load('y_1');
X = X(1:212,:);
y = y(1:211,:);
y = y(:,15);
t_X = [];
for i=1:n_aqi
    t = (X(:,4*final(i))~=-1);
    if (t(1)==1)
        t_X=[t_X X(2:212,4*final(i)-2:4*final(i)+1)];
    end
end

[M,N] = size(t_X);
for i = 1:N
    mi = min(t_X(:,i));
    if (mi == -1)
        mi = 0;
    end
    ma = max(t_X(:,i));
    t_X(:,i) = (t_X(:,i)-mi)/(ma-mi)
end
y = X(1:211,54)
data = [y t_X];
train_data = data(1:155,:);
test_data = data(156:211,:);    
save train_data train_data
save test_data test_data
%[TrainingTime,TrainingAccuracy]  = elm_train('train_data', 1, 10, 'sig')
Tr_error=0;
Te_error=0;
for iter = 1:500
    [TrainingTime, TestingTime, TrainingAccuracy, TestingAccuracy] = elm('train_data','test_data', 0,20 , 'sig');
    Tr_error=Tr_error+TrainingAccuracy;
    Te_error=Te_error+TestingAccuracy;
end
Tr_error=Tr_error/500;
Te_error=Te_error/500;
fprintf('Tr_error = %f, Te_error = %f\n',Tr_error,Te_error);

end

