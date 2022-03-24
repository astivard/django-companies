ymaps.ready(init);

var placemarks = JSON.parse(document.getElementById('placemarks_data_list').textContent);
geoObjects = [];

function init() {
  var map = new ymaps.Map('map', {
      center: [52.42, 31.02],
      zoom: 11,
      controls: ['zoomControl', 'fullscreenControl', ],
  });

  for (var i = 0; i < placemarks.length; i++) {
          geoObjects[i] = new ymaps.Placemark([placemarks[i].latitude, placemarks[i].longitude],
          {
              iconCaption: placemarks[i].iconContent,
              balloonContentHeader: `${placemarks[i].hintContent}`,
              balloonContentHeader: placemarks[i].iconContent,
              balloonContentBody: `<big>${placemarks[i].hintContent}</big>`,
          },
          {
              preset: 'islands#dotIcon',
          });
  }

  var clusterer = new ymaps.Clusterer({
  });

  map.geoObjects.add(clusterer);
  clusterer.add(geoObjects);
}
