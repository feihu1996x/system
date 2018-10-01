/*
 * @file:  index.js
 * @brief:  公共函数
 * @author: feihu1996.cn
 * @date:  18.09.22
 * @version: 1.0
*/

import * as event  from './event.js';

export default { event };

export const buildUrl = function( path,params ){
    var url = path;
    var _paramUrl = "";
    if(  params ){
        _paramUrl = Object.keys( params ).map( function( k ){
            return [ encodeURIComponent( k ),encodeURIComponent( params[ k ] ) ].join("=");
        }).join("&");
        _paramUrl = "?" + _paramUrl;
    }
    return url + _paramUrl;
}
