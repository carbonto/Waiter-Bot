var twist;
var cmdVel;
var publishImmidiately = true;
var robot_IP;
var manager;
var teleop;
var ros;

var battery_status;
var loadfoodClient;

var LoadFood_STATE_READY = "LOAD FOOD"
var LoadFood_STATE_LOADING = "Calibrating..."


function moveAction(linear, angular) {
    if (linear !== undefined && angular !== undefined) {
        twist.linear.x = linear;
        twist.angular.z = angular;
    } else {
        twist.linear.x = 0;
        twist.angular.z = 0;
    }
    cmdVel.publish(twist);
}

function initVelocityPublisher() {
    // Init message with zero values.
    twist = new ROSLIB.Message({
        linear: {
            x: 0,
            y: 0,
            z: 0
        },
        angular: {
            x: 0,
            y: 0,
            z: 0
        }
    });
    // Init topic object
    cmdVel = new ROSLIB.Topic({
        ros: ros,
        name: '/cmd_vel',
        messageType: 'geometry_msgs/Twist'
    });
    // Register publisher within ROS system
    cmdVel.advertise();
}


function initTeleopKeyboard() {
    // Use w, s, a, d keys to drive your robot

    // Check if keyboard controller was aready created
    if (teleop == null) {
        // Initialize the teleop.
        teleop = new KEYBOARDTELEOP.Teleop({
            ros: ros,
            topic: '/cmd_vel'
        });
    }

    // Add event listener for slider moves
    robotSpeedRange = document.getElementById("robot-speed");
    robotSpeedRange.oninput = function () {
        teleop.scale = robotSpeedRange.value / 100
    }
}


// Setup battery status
// Subscribing to a Topic
function setBattery(battery_status) {
    console.log('SetBattery Started');
    


    var listener = new ROSLIB.Topic({
        ros : ros,
        name : '/battery',
        messageType : 'std_msgs/Float32'
    });

    listener.subscribe(function(message) {
    console.log('Received message on ' + listener.name + ': ' + message.data);
    battery_status.style = "width:"+message.data+"%";
    battery_status.innerHTML = message.data + '%';
    //listener.unsubscribe();
    });

    console.log('SetBattery Finished');
}

function setLoadFoodBtn() {
    console.log('Load Food Initialised');
    loadfood_btn = document.getElementById('loadfood-btn');
    $( "#loadfood-btn" ).click(function(event) {
        console.log('Load Food Clicked');
        event.preventDefault(); // To prevent following the link (optional)
        if (loadfood_btn.innerHTML == LoadFood_STATE_READY){
            loadfood_btn.innerHTML = LoadFood_STATE_LOADING;
            $(loadfood_btn).removeClass("btn-success");
            $(loadfood_btn).addClass("btn-warning");
            load_food_results = LoadFood();
            
        }else{
            console.log('CALIBRATING STATUS='+loadfood_btn.innerHTML);
        }
        
         
      });

}

// Calling a service
/*
function LoadFood(loadfoodClient){
    loadfoodClient = new ROSLIB.Service({
        ros : ros,
        name : '/loadfood_server',
        serviceType : 'std_srvs/Trigger'
      });


    var request = new ROSLIB.ServiceRequest({});
    var success_value;
    var message_value;
    loadfoodClient.callService(request, function(result) {
        success_value = result.success;
        message_value = result.message;
        console.log('Result for service call on '
            + loadfoodClient.name
            + ': '
            + success_value
            + ':'
            + message_value);
        console.log('Load Food Finished');
        loadfood_btn = document.getElementById('loadfood-btn');
        $(loadfood_btn).removeClass("btn-warning");
        $(loadfood_btn).addClass("btn-success");        
        loadfood_btn.innerHTML = LoadFood_STATE_READY; 
    });

    

    return [success_value, message_value];
}
*/
function setMoveToTableBtn() {
    console.log('Move To Table Initialised');
    
    $(".btn-table").click(function(event2){
        // Holds the product ID of the clicked element
        event2.preventDefault(); // To prevent following the link (optional)
        var tableId = this.id;
        var res = tableId.split("-");
        var table_number = res[1];

        var tableinnerHTML = this.innerHTML;
        console.log("Generic Table ID===>"+tableId);
        console.log("Generic Table innerHTML===>"+tableinnerHTML);

        table_btn = document.getElementById(tableId);
        event2.preventDefault(); // To prevent following the link (optional)
        //if (table_btn.innerHTML == "T1"){
        if ($(this).hasClass( 'active' )){
            console.log('MOVING to Table='+table_number);            
        }else{
            table_btn.innerHTML = "MOVING TO T"+table_number;
            $(this).toggleClass('active');
            $(table_btn).removeClass("btn-success");
            $(table_btn).addClass("btn-warning");
            MoveToTable(parseInt(table_number));
            
        }
        
      });

}

// Calling action
function MoveToTable(table_number){

    var moveToTableClient = new ROSLIB.ActionClient({
        ros : ros,
        serverName : '/move_to_table_as',
        actionName : 'actionlib/TestAction'
      });

    var goal = new ROSLIB.Goal({
    actionClient : moveToTableClient,
    goalMessage : {
        goal : table_number
    }
    });
    
    goal.on('feedback', function(feedback) {
        console.log('Feedback: ' + feedback.feedback);
        movetotable_progress = document.getElementById('movetotable-progress');
        movetotable_progress.style = "width:"+feedback.feedback+"%";
        movetotable_progress.innerHTML = feedback.feedback + '%';
    });
    
    goal.on('result', function(result) {
        console.log('Final Result: ' + result.result);
        table_btn = document.getElementById('table-'+table_number+'-btn');
        $(table_btn).removeClass("btn-warning");
        $(table_btn).addClass("btn-success");
        $(table_btn).toggleClass('active');   
        table_btn.innerHTML = "T"+table_number;
        movetotable_progress = document.getElementById('movetotable-progress');
        movetotable_progress.style = "width:0%";
        movetotable_progress.innerHTML = '0%';
        success_value = result.result
    });

    
    goal.send();
    
    
    $( "#table-cancel-btn" ).click(function(event3) {
        console.log('Cancel Move Clicked');
        event3.preventDefault();
        moveToTableClient.cancel();
            
        });
    


}


  


window.onload = function () {
    // determine robot address automatically
    robot_IP = location.hostname;
    // set robot address statically
    //robot_IP = "10.5.10.117";

    // // Init handle for rosbridge_websocket
    ros = new ROSLIB.Ros({
        url: "ws://localhost:9090"
        //url: "ws://" + robot_IP + ":9090"
    });

    ros.on('connection', function() {
        console.log('Connected to websocket server.');
    });
    
    ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
    });

    ros.on('close', function() {
    console.log('Connection to websocket server closed.');
    });
    
    

    initVelocityPublisher();
    // get handle for video placeholder
    video = document.getElementById('video');
    // Populate video source 
    video.src = "http://" + robot_IP + ":8080/stream?topic=/pan_and_tilt/main_cam/image_raw&type=mjpeg&quality=80";
    video.onload = function () {
        // joystick and keyboard controls will be available only when video is correctly loaded
        initTeleopKeyboard();
    };

    // get handle for video placeholder
    battery_status = document.getElementById('battery-status');
    battery_status.style = "width:10%";
    battery_status.innerHTML = '10%';
    setBattery(battery_status);

    
    //loadfood = document.getElementById('loadfood-btn');
    setLoadFoodBtn();

    // Start the Move to table action client
    setMoveToTableBtn();
    
    
}