let navbar = document.querySelector('.header .navbar');
let account = document.querySelector('.header .account-box');
var productManage = angular.module("productBS", []);

document.querySelector('#menu-btn').onclick = () => {
    navbar.classList.toggle('active');
    account.classList.remove('active');
}
document.querySelector('#user-btn').onclick = () => {
    account.classList.toggle('active');
    navbar.classList.remove('active');
}

window.onscroll = () => {
    navbar.classList.remove('active');
    account.classList.remove('active');
}
// document.querySelector('#close-update').onclick = () => {
//     document.querySelector('.edit-product-form').style.display = 'none';
//     // window.location.href = 'admin_product.html';
// }
productManage.controller("controlProduct", ['$scope', function ($scope) {
    $scope.productTemplate = [{
        'name': 'Apple',
        'catg': ['A01', 'A02', 'A03']
    },
    {
        'name': 'Samsung',
        'catg': ['S01', 'S02', 'S03', 'S04', 'S05']
    },
    {
        'name': 'LG',
        'catg': ['LG01', 'LG02']
    },
    {
        'name': 'Sony',
        'catg': ['SO_01', 'SO_02']
    }
    ];
    $scope.userCart = [];
    $scope.addToCart = function ($this) {
        for (item of $scope.userCart) {
            if (item.proPrice == $this.proPrice && item.proName == $this.proName && item.proCatName == $scope.productTemplate[$this.proCatName]['name'] && item.proCatType == $this.proCatType) {
                item.proQuantity += $this.proQuantity;
                item.proTotal += $this.proQuantity * $this.proPrice;
                return;
            }
        }
        $scope.userCart.push({
            'proName': $this.proName,
            'proCatName': $scope.productTemplate[$this.proCatName]['name'],
            'proCatType': $this.proCatType,
            'proPrice': $this.proPrice,
            'proQuantity': $this.proQuantity,
            'proTotal': $this.proPrice * $this.proQuantity
        });
    };
    $scope.sendToUp = function ($idx) {
        $scope.checkCart = true;
        $scope.temp = $idx;
    };
    $scope.updateCart = function ($this) {
        $scope.userCart[$scope.temp]['proName'] = $this.proName_1;
        $scope.userCart[$scope.temp]['proCatName'] = $scope.productTemplate[$this.proCatName_1]['name'],
            $scope.userCart[$scope.temp]['proCatType'] = $this.proCatType_1;
        $scope.userCart[$scope.temp]['proPrice'] = $this.proPrice_1;
        $scope.userCart[$scope.temp]['proQuantity'] = $this.proQuantity_1;
        $scope.userCart[$scope.temp]['proTotal'] = ($this.proPrice_1) * $this.proQuantity_1;

        let present = $scope.userCart[$scope.temp];
        for (var i = 0; i < $scope.userCart.length; i++) {
            let item = $scope.userCart[i];
            if (i != $scope.temp && item['proPrice'] == present['proPrice'] && item['proName'] == present['proName'] && item['proCatName'] == present['proCatName'] && item['proCatType'] == present['proCatType']) {
                $scope.userCart[i]['proQuantity'] += present['proQuantity'];
                $scope.userCart[i]['proTotal'] += present['proQuantity'] * present['proPrice'];
                $scope.userCart.splice($scope.temp, 1);
                console.log($scope.userCart);
                $scope.temp = -1;
                return;
            }
        }
        $scope.temp = -1;
    };
    $scope.deletePro = function ($idx) {
        if (confirm("Delete this product?")) {
            $scope.userCart.splice($idx, 1);
        }
    };

}]);