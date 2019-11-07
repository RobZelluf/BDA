data {
  int<lower=0> N; // Number of variables
  int<lower=0> M; // Number of data points
  matrix[N, M] x;
  int<lower=0,upper=1> y[M];
}
parameters {
  vector[N] W;
  real b;
}
model {
  for (m in 1:M)
    y[m] ~ bernoulli_logit(W' * x[:,m] + b);
}

