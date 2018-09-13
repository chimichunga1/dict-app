app.controller('listdata',function($scope, $http){

    LoadAllData = function(){
      $http({
            url: '/falcon/things',
            method: "GET",
            })
        .then(function(response) {
            $scope.doc = response.data;
    });
  };

  LoadAllData();


  $scope.users = []; //declare an empty array

  
  $scope.sort = function(keyname){
    $scope.valueten = 6;
    $scope.sortKey = keyname;   //set the sortKey to the param passed
    $scope.reverse = !$scope.reverse; //if true make it false and vice versa
    $scope.itemsPerPage = $scope.valueten;
  }
});


//================================================//
app.controller('addCtrl', function($scope, $http) {
     $http({
        url:'https://restcountries.eu/rest/v2/all',
        method:'GET'
          })
     .then(function(response) {
        $scope.doc_countries = response.data;
    });
});

//================================================//

app.controller('dictionary_list', function($scope, $http, $filter, $mdToast, $mdDialog) {
  LoadAllData = function(){
      $http({
            url: '/falcon/things',
            method: "GET",
            })
        .then(function(response) {
            $scope.doc = response.data;
    });
  };

  SetLimit = function(){

    if($scope.pageSize == null){
      $scope.pageSize =5;
    };    
  };


  ClearInput = function(){
  $scope.chips={}
  $scope.chips.job_title=[];
  $scope.chips.synonymous=[];
  $scope.chips.misspell=[];
  $scope.chips.suggestion=[];

  }


  SetLimit();
  LoadAllData();
  









//==PAGINATION FUNCTION==========//
  $scope.page = 1;

  
  $scope.pageChanged = function() {
    var startPos = ($scope.page - 1) * 3;
    //$scope.displayItems = $scope.totalItems.slice(startPos, startPos + 3);
    console.log($scope.page);
  };
//==PAGINATION FUNCTION==========//
  $scope.sort = function(keyname){
    $scope.sortKey = keyname;   //set the sortKey to the param passed
    $scope.reverse = !$scope.reverse; //if true make it false and vice versa
  }
//CHANGE FUNCTION FOR LIMIT BY OPTION//
$scope.change = function(){
    $NumPerPage = $scope.pageSize;
    console.log($scope.pageSize);
};
//CHANGE FUNCTION FOR LIMIT BY OPTION//

  $scope.chips={}
  $scope.chips.job_title=[];
  $scope.chips.synonymous=[];
  $scope.chips.misspell=[];
  $scope.chips.suggestion=[];
  $scope.AddNewDictForm = function(){

    if($scope.chips.job_title == '' || $scope.chips.synonymous == '' || $scope.chips.misspell == '' || $scope.chips.suggestion == ''){

      swal({
        type: 'error',
        title: 'Oops...',
        text: 'Fields must not be empty!',
  
      })
    }
    else
    {
    $scope.doc = [];
    $scope.doc.push($scope.chips.job_title,$scope.chips.synonymous,$scope.chips.misspell,$scope.chips.suggestion);
        $http({
          url: '/falcon/AddNewDict',
          method: "POST",
          data: $scope.doc
              })
      .then(function(response) {
       LoadAllData();
       ClearInput();
   });





    swal(
  'Sucess!',
  'You saved a new Data!',
  'success'

)


 var isDlgOpen;



      $scope.closeToast = function() {
        if (isDlgOpen) return;

        $mdToast
          .hide()
          .then(function() {
            isDlgOpen = false;
          });
      };

  }
};

//================WILFRED WILFRED WILFRED WILFRED ======================//
     $scope.newEditDict = function(data) {
      $scope.send={}
      $scope.send.display=data.display;
      $scope.send._id=data._id;
      $scope.send.synonymous=[];
      $scope.send.misspell=[];
      $scope.send.suggestion=[];
        for(var i=0;i<data.synonymous.length;i++) {
        $scope.send.synonymous.push(data.synonymous[i]);
          }
      for(var i=0;i<data.misspell.length;i++) {
      $scope.send.misspell.push(data.misspell[i]);
      }
      for(var i=0;i<data.suggestion.length;i++) {
      $scope.send.suggestion.push(data.suggestion[i]);
      }
  }
     $scope.newEditDictForm = function() {
      $http({
          url: '/falcon/UpdateAll',
          method: "POST",
          data: $scope.send
            })
      .then(function(response) {
                LoadAllData();

      });

    swal(
  'Sucess!',
  'You updated a Data!',
  'success'
)



  }
//================WILFRED WILFRED WILFRED WILFRED ======================//
//================================================//
     $scope.deleteDictForm = function() {

      $http({
          url: '/falcon/getDelete',
          method: "POST",
          data: $scope.getData
            })
      .then(function(response) {
        LoadAllData();
    });



    swal(
  'Success!',
  'You deleted the data!',
  'success'
)

}
//================================================//
     $scope.deleteDict = function(data){
      $scope.getData = data;
}
//================================================//
     $scope.editDict = function(data){
      $scope.getId = data.id;
      $scope.keywords = data.value.misspell;      
      $scope.syno = data.value.synonymous;
      $scope.job_title = data.value._id;
}
//================================================//
     $scope.addDict = function(data){
      $scope.getId = data.id;
      $scope.keywords = data.value.misspell;      
      $scope.syno = data.value.synonymous;
      $scope.job_title = data.value._id;
}
//================================================//
      $scope.deleteSyno = function(data) { 
        var index = $scope.syno.indexOf(data);
        $scope.removeSyno = {'syno':data,'id':$scope.getId};
        $scope.syno.splice(index, 1);
        $http({
              url: '/falcon/delSyno',
              method: "POST",
              data: $scope.removeSyno
              })
        .then(function(response) {
          
              });
}
//================================================//
      $scope.deleteKeywords = function(data) { 
        console.log(data);
        var index = $scope.keywords.indexOf(data);
        $scope.removekeyword = {'keywords':data,'id':$scope.getId};
        $scope.keywords.splice(index, 1);  

        $http({
              url: '/falcon/delKeywords',
              method: "POST",
              data: $scope.removekeyword
              })
          .then(function(response) {

              });
}
//================================================//
      $scope.UpdateSyno = function(data,placeholder) { 
        $scope.CurrentSyno = placeholder // orig value
        $scope.NewSyno = data //new value
        console.log(placeholder)
        $scope.updateSyno = {'CurrentSyno':placeholder,'NewSyno':data,'id':$scope.getId};
        console.log($scope.updateSyno);
        $http({
              url: '/falcon/UpdateSyno',
              method: "POST",
              data: $scope.updateSyno
              })
          .then(function(response) {
          
              });
}
//================================================//
      $scope.updateKeywords = function(data,placeholder) { 
        $scope.CurrentKeyword = placeholder // orig value
        $scope.NewKeyword = data //new value
        console.log(placeholder)
        $scope.updateKeyword = {'CurrentKeyword':placeholder,'NewKeyword':data,'id':$scope.getId};
        console.log($scope.updateKeyword);
        $http({
              url: '/falcon/UpdateKeywords',
              method: "POST",
              data: $scope.updateKeyword
              })
        .then(function(response) {
              console.log("UpdateKeyword");
              });
          
}
//================================================//

      $scope.UpdateJobTitle = function(data) { 
        $scope.UpdateJobTitle = {'job_title':data,'id':$scope.getId};
        $http({
              url: '/falcon/UpdateJobTitle',
              method: "POST",
              data: $scope.UpdateJobTitle
          })
          .then(function(response) {
              console.log("UpdateJobTitle");
          });
}
//================================================//
  $scope.SynonymModal = [{}];
      $scope.AddSynonymModal = function() {
        var SynonymItem = $scope.SynonymModal.length+1;
        $scope.SynonymModal.push({SynonymItem});
 
  };
//================================================//
      $scope.RemoveSynonymModal = function() {
        var SynonymItemLast = $scope.SynonymModal.length-1;
        $scope.SynonymModal.splice(SynonymItemLast);
  };
//================================================//
  $scope.KeywordModal = [{}];
      $scope.AddKeywordModal = function() {
        var KeywordItem = $scope.KeywordModal.length+1;
        $scope.KeywordModal.push({KeywordItem});

  };
//================================================//
      $scope.RemoveKeywordModal = function() {
        var KeywordItemLast = $scope.KeywordModal.length-1;
        $scope.KeywordModal.splice(KeywordItemLast);
  };
//================================================//
 $scope.addDictForm = function() {
  $scope.doc=[];
  $scope.doc.push($scope.SynonymModal,$scope.KeywordModal,$scope.getId);
  $http({
        url: '/falcon/addSynoKey',
        method: "POST",
        data: $scope.doc
    })
    .then(function(response) {
    console.log('yes');
    });
  }
});
//================================================//


