% Example ODE45 evaluation of a mass-spring-damper system provided in the
% notes in class.
%
% m-files needed: MSD.m
%
% Last modified: 05 October 2021

close all;

%% Specify time range of interest and intial conditions
tspan=[0 30];   % Time range, [s]
x0=[7.5;0];       % Initial momentum and displacement

%% Integrate state-space equations
[t,x] = ode45(@MSD,tspan,x0);
[t2,x2] = ode45(@MSD2,tspan,x0);
%% Convert momentum state variable to the velocity of the mass
I=1;        % Mass, [kg]
qdot=x(:,1)/I;

%% Plot results
figure
plot(t,x(:,2),t2,x2(:,2))
title('Spring-Mass-Damper Response Case 7 & 8')
xlabel('Time, [s]')
ylabel('Displacement, [m]')
legend('Case 7', 'Case 8')
grid on
x(length(x),2)
x2(length(x2),2)
% figure
% plot(t,qdot)
% title('Spring-Mass-Damper Response')
% xlabel('Time, [s]')
% ylabel('State Variable')
% legend('x','v')