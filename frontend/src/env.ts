const env = process.env.VUE_APP_ENV || "dev";
const prefix = process.env.VUE_APP_PREFIX || "/api/v1";
const dep_api = process.env.VUE_APP_API_DEV || "http://localhost:8080";
const this_host_api = process.env.VUE_APP_THIS_HOST_API;
console.log('prefix: ', prefix)
console.log('this_host_api: ', this_host_api)

let envApiUrl = '';
console.log("window.location.origin: ", window.location.origin)
console.log('ENV: ', env);
console.log("Api address: ", envApiUrl);
 if (env === 'production') {
  if (this_host_api === 'true') {
    envApiUrl = window.location.origin;
  } else {
    envApiUrl = `${process.env.VUE_APP_API_PROD}`;
  }
} else if (env === 'staging') {
  envApiUrl = `${process.env.VUE_APP_API_STAG}`;
} else {
  envApiUrl = dep_api;
}

console.log("Api address: ", envApiUrl);

export const apiUrl = envApiUrl;
export const prefixUrl = prefix;

