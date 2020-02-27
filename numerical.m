clear all
% parameter value
lambda_0 = 200; % 600 arrivals per hour, 200 per zone
mu = 0.25; % 15/60 = 0.25
theta = 100;
c_f = 100; % fixed cost
xi = 1; % deployment cost
gamma = 50; % rebalancing parameter
T = 5; % 5 hour per bucket

p_list = [0.20, 0.25, 0.30];
c_list = [1/6000, 1/3000, 1/1500, 1/1000, 1/500];
e_list = [0, 0.25, 0.5, 0.75, 1];

% plot over different prices
p = 0.25;
c = 1/1500;
% e = 0;
V_list = zeros(81, 1);
V_approx_list = zeros(29, 1);
N_axis = 100 : 50 : 1500;

for e = e_list
    for N = 100:50:1500
        i = (N - 100)/50 + 1;
        V_approx_list(i) = value_approx(N, T, lambda_0, mu, theta, c_f, xi, gamma, p, c, e);
    end
    plot(N_axis, V_approx_list);
    hold on
end
title({'Value function for different efforts';
    '\lambda_0 = 600, mu = 0.25, theta = 100, gamma = 50, p = 0.25, c = 1/1500'});
xlabel('Number of Scooters');
ylabel('Value');
legend('0','0.25','0.5','0.75','1','Location','SouthEast');
hold off


% for N = 100 : 50 : 1500
%     i = (N-100)/50 + 1;
%     %V_list(i) = value(N, T, lambda_0, mu, theta, c_f, xi, gamma, p, c, e);
%     V_approx_list(i) = value_approx(N, T, lambda_0, mu, theta, c_f, xi, gamma, p, c, e);
% end
% 
% figure();
% plot(N_axis, V_approx_list);
% title({'Value function';
%     '\lambda_0 = 200, mu = 0.25, theta = 100, gamma = 1, p = 0.25, c = 1/1500, e = 0'});
% xlabel('Number of Scooters');
% ylabel('Value');
% hold on
% plot(N_axis, V_approx_list);
% legend('Approx');
% legend('True', 'Approximation');
% hold off

% for N = 30 : 1 : 100
%         i = (N-30)/1 + 1;
%         V_list(i) = value(N, T, lambda_0, mu, theta, c_f, xi, gamma, 0.15, c, e);
% end
% figure();
% hold on
% plot(N_axis, V_list)
% title({'Value function for different prices';
%     '\lambda_0 = 600, mu = 0.25, gamma = 0.5, c = 0.04, e = 0.5'});
% xlabel('Number of Scooters');
% ylabel('Value');
% hold on
% 
%  for p = p_list
%      for N = 30 : 1 : 100
%          i = (N-30)/1 + 1;
%          V_list(i) = value(N, T, lambda_0, mu, theta, c_f, xi, gamma, p, c, e);
%      end
%      plot(N_axis, V_list)
% end
% legend('0.15', '0.20', '0.25', '0.30');
% hold off
