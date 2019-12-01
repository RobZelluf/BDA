data {
    int<lower=1> J;     // num of explanatory variables
    int<lower=0> N;     // num of obs
    vector[J] x[N];     // x is array of size N containing vectors of J elements
    vector[N] y;     // y is outcome variable
}
parameters {
    vector[J] beta;     // weight vector
    real Sigma;    // 
}
model {
    vector[N] mu;
    for (n in 1:N){
        mu[n] = beta * x[n];
    }
    y ~ multi_normal(mu, Sigma);
}

data {
    int<lower=1> K;     // num of outcomes
    int<lower=1> J;     // num of explanatory variables
    int<lower=0> N;     // num of obs
    vector[J] x[N];     // x is array of size N containing vectors of J elements
    vector[K] y[N];     // y is array of size N containing vectors of K elements
}
parameters {
    matrix[K, J] beta;     // K x J matrix
    cov_matrix[K] Sigma;    // 
}

model {
    vector[K] mu[N];

    for (n in 1:N){
        mu[n] = beta * x[n];
    }
    y ~ multi_normal(mu, Sigma);
}