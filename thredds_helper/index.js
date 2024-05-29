const http = require('http');
const httpProxy = require('http-proxy');
const request = require('request');

const port = 8089;
const username = 'inkode';
const password = process.env.THREDDS_PASSWORD ?? '';
const proxy_url = 'https://thredds.arpa.veneto.it/';
const proxy_external_url = process.env.PROXY_URL || 'http://localhost:8089/';
const auth = new Buffer.from(username + ':' + password).toString('base64');

async function get(url) {
   // Return new promise
   return new Promise(function (resolve, reject) {
      const headers = {
            'Authorization': 'Basic ' + auth
         };
      if(CookieObject.cookie) {
         headers['Cookie'] = CookieObject.cookie;
      }
      // Do async job
      request.get({
         url: url,
         followRedirect: true,
         followRedirects: true,
         followAllRedirects: true,
         headers: headers,
      }, function (err, resp, body) {
         console.log(resp.headers);
         const cookie = resp.headers['set-cookie'][0].split(';')[0];
         if (err) {
            reject(cookie);
         } else {
            resolve(cookie);
         }
      })
   })
}

const restrictedServices = [
   '/thredds/wms/',
   '/thredds/catalog/ens14ym/catalog.html',
   '/thredds/dodsC/ens14ym/pr_anom_pp_ts_rcp26_DJF.nc.html',
   '/thredds/restrictedAccess/dati_accordo',
];


const proxy = httpProxy.createProxyServer({
   target: proxy_url,
   changeOrigin: true,
   // followRedirects: true
});

class Singleton {
   constructor() {
      this.cookie = false;
   }
}

const CookieObject = new Singleton();

const getCookie = async () => {
   if (!this.cookie) {
      const url = proxy_url + 'thredds/dodsC/ens14ym/pr_anom_pp_ts_rcp26_DJF.nc.html';
      console.log(url);
      CookieObject.cookie = await get(url);
   }
   console.log('=================================================');
   console.log(CookieObject.cookie);
   return CookieObject.cookie;
}

var enableCors = function (req, res) {
   if (req.headers['access-control-request-method']) {
      res.setHeader('access-control-allow-methods', req.headers['access-control-request-method']);
   }

   if (req.headers['access-control-request-headers']) {
      res.setHeader('access-control-allow-headers', req.headers['access-control-request-headers']);
   }

   if (req.headers.origin) {
      // res.setHeader('access-control-allow-origin', req.headers.origin);
      res.setHeader('access-control-allow-origin', '*');
      res.setHeader('access-control-allow-credentials', 'true');
   }
};
// getCookie().then((cookie) => {
   proxy.on('proxyReq', function (proxyReq, req, res, options) {
      proxyReq.setHeader('cookie', CookieObject.cookie);
   });
   proxy.on('proxyRes', function (proxyRes, req, res, options) {
      // console.log(proxyRes)
      // if(proxyRes.statusCode())
      if (proxyRes.headers['set-cookie']) {
         const cookie = proxyRes.headers['set-cookie'][0].split(';')[0];
         CookieObject.cookie = cookie;
         delete proxyRes.headers['set-cookie'];
      }
      if (proxyRes.headers['location']) {
         proxyRes.headers['location'] = proxyRes.headers['location'].replace(proxy_url, proxy_external_url);
         if(proxyRes.statusCode == 500) {
            proxyRes.statusCode = 302;
         }
      }
      enableCors(req, res);
   });
   const server = http.createServer(function (req, res) {
      if(CookieObject.cookie)
         req.headers.cookie = CookieObject.cookie;
      req.headers.authorization = 'Basic ' + auth;
      console.log(req.url);
      // if (restrictedServices.includes(req.url)) {
      //    proxy.web(req, res);
      // }

      try {
         proxy.web(req, res, function (e) {
            console.error(e);
            res.writeHead(500, {'Content-Type': 'text/plain'});
            res.end('Something went wrong. Please try again.');
         });
      } catch (e) {
         console.log(e);
      }
   });

   console.log("listening on port " + port);
   server.listen(port);
// });
