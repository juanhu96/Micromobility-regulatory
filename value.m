function V = value(N, T, lambda_0, mu, theta, c_f, xi, gamma, p, c, e)
    denominator = 0;
    numerator = 0;
    l = (1 - theta/N * (1 - e)) * lambda_0;
    for j = 0 : 1 : N
        % to avoid overflow
        factor = l^j / (factorial(j) * mu^j);
        denominator = factor + denominator;
        numerator = factor * (j * 60 * p - (N-j) * 60 * c) + numerator;
    end
    V = T * (numerator/denominator) - c_f - xi * N - gamma * sqrt(N) * e^3;
end