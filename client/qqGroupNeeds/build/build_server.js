/*
 * @file:  buid_server.js
 * @brief:  构建express服务
 * @author: feihu1996.cn
 * @date:  18.09.23
 * @version: 1.0
*/
const { exec } = require('child_process');
const fs = require('fs');
const config = require('../server/config');

console.log("将dist/index.html移动到server/views/index.ejs ...");
exec('rm -rf ./server/views/* && mv ./dist/index.html ./server/views/index.ejs -fv', (error) => {
    if (error) {
        console.error(`exec error: ${error}`);
        return;
    } 
    console.log("done");
    console.log("将所有静态文件移动到server/public/目录下...");    
    exec('rm -rf ./server/public/* && mv ./dist/static/* ./server/public/ -fv && cp ./static/favicon.ico ./server/public/ -fv', (error) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return;
        }
        console.log("done");
        console.log("删除dist文件夹...");
        exec('rm -rf ./dist', (error) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return;
            }
            console.log("done");
            console.log("调整server/views/index.ejs文件内容...");
            var content = '';
            console.log("读取server/views/index.ejs文件内容...");            
            fs.readFile('./server/views/index.ejs', {flag: 'r+', encoding: 'utf8'}, function (err, data) {
                if(err) {
                    console.error(err);
                    return;
                }
                content = data;
                console.log("done:", content);
                console.log("替换content...");
                content = content.replace( /href=/g, "href=<%= url_prefix %>" ).replace( /src=/g, "src=<%= url_prefix %>");
                console.log("done:", content);
                console.log("将content写入./server/views/index.ejs文件...");
                fs.writeFile('./server/views/index.ejs', content,  function(err) {
                    if (err) {
                        return console.error(err);
                    }
                    console.log("done");
                    console.log( '正在统一url前缀...' );
                    fs.readFile('./src/api/api.js', {flag: 'r+', encoding: 'utf8'}, function (err, data) {
                        if (err) {
                            return console.error(err);
                        }
                        content = data;
                        url_prefix_pattern = /ROUTE_PREFIX = "(.*?)";/;
                        url_prefix = url_prefix_pattern.exec( content )?url_prefix_pattern.exec( content )[1]:"";
                        if ( null === url_prefix ){
                            console.error( "url_prefix not found" );
                            return;
                        }
                        fs.readFile('./server/config.js', {flag: 'r+', encoding: 'utf8'}, function (err, data) {
                            if( err ){
                                return console.error(err);
                            }
                            content = data;
                            content = content.replace( /url_prefix: ".*?"/, `url_prefix: "${url_prefix}"` );
                            fs.writeFile('./server/config.js', content,  function(err) {
                                if (err) {
                                    return console.error(err);
                                }
                                console.log("done");
                            });
                        });
                    });
                });
            });
        });        
    });
});
