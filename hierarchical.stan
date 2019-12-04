//
// This Stan program defines a simple model, with a
// vector of values 'y' modeled as normally distributed
// with mean 'mu' and standard deviation 'sigma'.
//
// Learn more about model development with Stan at:
//
//    http://mc-stan.org/users/interfaces/rstan.html
//    https://github.com/stan-dev/rstan/wiki/RStan-Getting-Started
//

// The input data is a vector 'y' of length 'N'.
data {
  int<lower=0> N;             // number of data points
  int<lower=0> K;             // number of groups
  matrix[K, N] y;
}

// The parameters accepted by the model. Our model
// accepts two parameters 'mu' and 'sigma'.
parameters {
  real super_mu;
  real super_sigma;
  
  vector[K] mu;             // group means
  real<lower=0> sigma;      // common std
}

// The model to be estimated. We model the output
// 'y' to be normally distributed with mean 'mu'
// and standard deviation 'sigma'.
model {
  for (k in 1:K)
    mu[k] ~ normal(super_mu, super_sigma);
  
  for (k in 1:K)
    y[k] ~ normal(mu[k], sigma);
}
generated quantities {
  real ypred;
  real ypred2;
  real mu2;
  
  ypred = normal_rng(mu[6], sigma);
  mu2 = normal_rng(super_mu, super_sigma);
  ypred2 = normal_rng(mu2, sigma);
}




