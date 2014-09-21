function []  = Temporal_elm( )
%SELECT_CITY Summary of this function goes here
%   Detailed explanation goes here
%n_dist = 10;
%n_aqi = 8;

X = load('X_1');
y = load('y_2');
t_X = [X(1:263,4:7) X(1:263,9) X(1:263,13:15)];
y = y(1:263,15);

[M,N] = size(t_X);
for i = 1:N
    mi = min(t_X(:,i));
    ma = max(t_X(:,i));
    t_X(:,i) = (t_X(:,i)-mi)/(ma-mi);
end

data = [y t_X];
   

%[TrainingTime,TrainingAccuracy]  = elm_train('train_data', 1, 10, 'sig')
Tr_error=0;
Te_error=0;
for iter = 1:500
    rand = randperm(M);
    data=data(rand,:);  
    train_data = data(1:210,:);
    test_data = data(211:263,:);
    save train_data train_data
    save test_data test_data
    [TrainingTime, TestingTime, TrainingAccuracy, TestingAccuracy] = elm('train_data','test_data', 1,20 , 'sin');
    Tr_error=Tr_error+TrainingAccuracy;
    Te_error=Te_error+TestingAccuracy;
end
Tr_error=Tr_error/500;
Te_error=Te_error/500;
fprintf('Tr_error = %f, Te_error = %f\n',Tr_error,Te_error);

end

