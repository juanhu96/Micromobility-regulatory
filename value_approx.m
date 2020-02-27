function V = value_approx(N, T, lambda_0, mu, theta, c_f, xi, gamma, p, c, e)
    % an approximation of the original function
    l = (1 - theta/N * (1 - e)) * lambda_0;
    V = T * 60 * (p+c) * (l/mu) - T * N * 60 * c - c_f - xi * N - gamma * sqrt(N) * e^3;
end