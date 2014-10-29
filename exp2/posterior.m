function posterior( input_args )
%POSTERIOR Summary of this function goes here
%   Detailed explanation goes here
station = 'haidian';
col = 13;
left = 0;
right = 5;
f1 = ['data/' station '_decrease.txt'];
f0 = ['data/' station '_high.txt'];
d1 = load(f1);
d1 = d1(:,col);
d1 = d1(find(d1(:,1)~=-1),:);
d0 = load(f0);
d0 = d0(:,col);
d0 = d0(find(d0(:,1)~=-1),:);

d = [d0' d1']';

p_s = size(d1,1)/size(d,1)
p_x = size(find(d(:,1)>=left & d(:,1)<=right),1)/size(d,1)
p_x_s = size(find(d1(:,1)>=left & d1(:,1)<=right),1)/size(d1,1)
p_s_x = p_x_s*p_s/p_x;
fprintf('prior probability: %f, posterior probability: %f \n',p_s,p_s_x);
end

