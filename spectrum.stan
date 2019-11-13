data {
  int<lower=0> N; // Number of variables
  int<lower=0> M; // Number of data points
  matrix[M, N] x;
  real<lower=0,upper=1> y[M];
}
parameters {
  vector[N] W;
  real b;
  real sigma;
}
model {
  for (m in 1:M)
    y[m] ~ normal(x[m,] * W + b, sigma);
}

