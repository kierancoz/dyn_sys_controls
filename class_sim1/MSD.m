% This function evaluates the state-space equations at each time called by
% the ode45 function (or other integrator)

function xdot=MSD(t,x)

% Specify system parameters
R=0.5;        % Damping coefficient, [N.s/m] % 5, 15
I=1;        % Mass, [kg] % 1
C=1/20;    % Compliance, [m/N]
L0 = 0.5; % m
h = 0.95*L0;

%% Specify different types of forcing functions
% Step force on at t = 0
E1=0;

%% Force on, then off at t = 3
% if t<3
%     E1=2;       % Step force, [N]
% else
%     E1=0;
% end
% 
% %% Multiple force steps
% if t<2
%     E1=2;
% elseif t>6
%     E1=-4;
% else
%     E1=0;
% end

%% Look at linear and nonlinear examples
% Linear case
% A=[-R/I -1/C;
%    1/I 0];   
% b=[1;0];
% xdot=A*x+b*E1;

% Nonlinear case
damping = (R/I)*x(1);
%normal_force = I*9.81 + (x(2)^2+h^2)^(1/2)*(L0-(x(2)^2+h^2))^(1/2)/C;
%damping = 0.1*abs(normal_force)*sign(x(1));
xdot1 = E1-damping+x(2)*(L0-(x(2)^2+h^2)^(1/2))/((x(2)^2+h^2)^(1/2)*C);
xdot2 = (1/I)*x(1);

xdot=[xdot1;xdot2];



