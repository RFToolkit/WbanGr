var celticColor = "#7becb2",
  italicColor = "#ecb27b",
  indoIranianColor = "#ec7bb6";

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const chart=Highcharts.chart('container', {

  chart: {
    type: 'networkgraph',
    marginTop: 80
  },

  title: {
    text: 'IOT Observation en temp reel'
  },

  subtitle: {
    text: 'Neighbour devices'
  },

  plotOptions: {
    networkgraph: {
      keys: ['from', 'to'],
      layoutAlgorithm: {
        enableSimulation: true,
        integration: 'verlet',
        linkLength: 100
      }
    }
  },
  linkFormat: '{point} \u2192 {point}',

  series: [{
    marker: {
      radius: 13,
    },
    dataLabels: {
      enabled: true,
      linkFormat: '',
      allowOverlap: true
    },
    data: [],
    nodes: []
  },{
    marker: {
      radius: 9,
    },
    dataLabels: {
      enabled: true,
      linkFormat: '',
      allowOverlap: true
    },
    data: [],
    nodes: []
  }]
});

const pan = [];
const ids = [];

function isArrayInArray(arr, item){
  var item_as_string = JSON.stringify(item);

  var contains = arr.some(function(ele){
    return JSON.stringify(ele) === item_as_string;
  });
  return contains;
}

const bleUid = (response) => {
  response.forEach(resp => {
    console.log(String(resp['manufact']), "", String(resp['services']))
    chart.series[1].addPoint([resp.addr, resp.uuid[0]+",RSSI:"+resp.rssi], true)
  });
  
}
const getBle = () =>
  fetch('http://127.0.0.1:5000/getble', { mode: 'cors', headers: { 'Access-Control-Allow-Origin':'*' } })
    .then((response) => response.json())
    .then(bleUid);

let cpt = 0;

fetch('http://127.0.0.1:5000/getpkt', { mode: 'cors', headers: { 'Access-Control-Allow-Origin':'*' } })
    .then((response) => response.body)
    .then((body) => {
        const reader = body.getReader();
        reader.read().then(function processText({ done, value }) {
            /* … */
            console.log(value)
            
            if(value) {
                console.log(Array.from(value).map(x=> String.fromCharCode(x)).join(''))
                
                let payloads=Array.from(value).map(x=> String.fromCharCode(x)).join('').trim()
                
                payloads=Array.from(payloads.match(/{[^}]+}/g))
                payloads.forEach(payload => {
                    payload=JSON.parse(payload)
                    console.log(payload)
                    if (((payload.src != null && payload.dst != null) || (payload.src != null && payload.panid != null) || (payload.panid != null && payload.panid != null))) {
                      if (!isArrayInArray(pan, [payload.src, payload.dst])) {
                        pan.push([payload.src, payload.dst])

                        chart.series[0].addPoint([payload.src, payload.dst])
                        Promise.resolve(sleep(100));
                      }
                    }
                });
                
            }
            value=null
            if (done) return;
            return reader.read().then(processText);
        })
        // …
    });

    