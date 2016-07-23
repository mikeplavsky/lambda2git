'use strict';
console.log('Loading function');

const AWS = require('aws-sdk');
const l = new AWS.Lambda();

const call = (func,payload) => {
    
    l.invoke({
        
        FunctionName:func,
        Payload: payload
        
    }, (err,data)=>{
        
        console.log(
            JSON.parse(payload).AWS_LAMBDA);
        
        console.log(
            err);
        console.log(
            data);
        
    })
    
};

exports.handler = (event, context, callback) => {
    
    var msg = {
        GIT_USER: "<your name>",
        GIT_KEY : "<your key>",
        GIT_REPO: "GitQuest/aws-police"
    }
    
    let funcs = [
        "aws-cleaner-sg", 
        "iam_delete_access_keys", 
        "iam_delete_login_profile",
        "aws-command-teams",
        "aws-command-count",
        "aws-command-types",
        "aws-command-life",
        "spb-aws-status-async",
        "aws-command",
        "aws-command-worker"];
        
    funcs.forEach(fn => {
        
        msg.AWS_LAMBDA = fn;
        call("lambda2git", JSON.stringify(msg));
        
    });

    console.log("getting data...")
    
};
