//var server = "192.168.43.201";
var server = "localhost:8080";

var app = angular.module('tutorialWebApp', [
  'ngRoute'
]);

/**
 * Configure the Routes
 */
app.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    // Home
    .when("/", {templateUrl: "partials/home.html", controller: "PageCtrl"})
    // Pages
    .when("/about", {templateUrl: "partials/about.html", controller: "PageCtrl"})
    .when("/faq", {templateUrl: "partials/faq.html", controller: "PageCtrl"})
    .when("/pricing", {templateUrl: "partials/pricing.html", controller: "PageCtrl"})
    .when("/services", {templateUrl: "partials/services.html", controller: "PageCtrl"})
    .when("/contact", {templateUrl: "partials/contact.html", controller: "PageCtrl"})
    // Blog
    .when("/blog", {templateUrl: "partials/blog.html", controller: "BlogCtrl"})
    .when("/blog/post", {templateUrl: "partials/blog_item.html", controller: "BlogCtrl"})
    // else 404
    .otherwise("/404", {templateUrl: "partials/404.html", controller: "PageCtrl"});
}]);

/**
 * Controls the Blog
 */
app.controller('BlogCtrl', function (/* $scope, $location, $http */) {
  console.log("Blog Controller reporting for duty.");
});

var params = [];
var paramsString ="";
var step = 0;
app.controller('PageCtrl', function ($scope,$http) {

  $scope.title = params;
  //$scope.init = true;
  
  if(step == 0){
    $http.get("http://"+server+"?query=")
    .success(function(response){
      //$scope.init = false;
      step++;
      $scope.step=step;
      $scope.results = response.clusters;
      console.log(params);

    })
    .error(function(response){
      alert("Oupsss plus de serveur");
    })
    .finally(function(response) {
      //alert("error");
    }); 
  }

  /*
  if(step == 4){

    $http.get("http://192.168.43.201:8080?query=documents")
    .success(function(response){ 
      $scope.results = [];
      $scope.documents = response.documents;
      console.log(params);

    })
    .error(function(response){
      alert("Oupsss plus de serveur");
    })
    .finally(function(response) {
      //alert("error");
    }); 
  }
  */

  else{

    $scope.loading = true;

    $http.get("http://"+server+"?query="+paramsString)
    .success(function(response){

      $scope.loading = false;

      if(response.clusters != null){
        $scope.results = response.clusters;
      }else{
        $scope.documents = response.documents;
      }
  
      //$scope.results = response.clusters;
      //console.log(params);

    })
    .error(function(response){
      alert("Oupsss plus de serveur");
    })
    .finally(function(response) {
      //alert("error");
    }); 
  }

  $scope.step=step;
  step++;


   $scope.clickEvent = function(mot){
      params.push(mot);
      paramsString+=mot + " ";
   }

   $scope.clickInit = function(){
    //$scope.init = true;
    step = 0
   }

   console.log(paramsString);

});