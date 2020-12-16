var Example = Example || {};

var json_data = [];
var url = "http://127.0.0.1:5000/uploads/";

// $.getJSON('../todo-list.json',function(data){
//     for(let i=0; i < data.length; i++){
//         json_data.push(data[i]["content"]);
//     }
// });


function init(app_route="/get") {
    // データの初期表示
    fetch(app_route).then(response => {
        console.log(response)
        response.json().then((data) => {
            console.log(data);
        })
    })
}





// htmlのページを読み込まれたときに処理をする
window.onload = function() {
    var Engine = Matter.Engine,
        Render = Matter.Render,
        Runner = Matter.Runner,
        Composites = Matter.Composites,
        Common = Matter.Common,
        MouseConstraint = Matter.MouseConstraint,
        Mouse = Matter.Mouse,
        World = Matter.World,
        Bodies = Matter.Bodies;

    // create engine
    var engine = Engine.create(),
        world = engine.world;

    // create renderer
    var render = Render.create({
        element: document.body,
        engine: engine,
        options: {
            width: 800,
            height: 600,
            background: '#0f0f13',
            showAngleIndicator: false,
            wireframes: false
        }
    });

    Render.run(render);

    // create runner
    var runner = Runner.create();
    Runner.run(runner, engine);

    // add bodies
    var offset = 10,
        options = { 
            isStatic: true
        };

    world.bodies = [];

    // these static walls will not be rendered in this sprites example, see options
    World.add(world, [
        Bodies.rectangle(400, -offset, 800.5 + 2 * offset, 50.5, options),
        Bodies.rectangle(400, 600 + offset, 800.5 + 2 * offset, 50.5, options),
        Bodies.rectangle(800 + offset, 300, 50.5, 600.5 + 2 * offset, options),
        Bodies.rectangle(-offset, 300, 50.5, 600.5 + 2 * offset, options)
    ]);
    
     //<<JSONを読み込む　未実装　はじまり>>
    // ###--要素作成--###
    //jsonまたはページ上のデータを直接読み込み


    // json_data = fetch("./todo-list.json")
    // .then(response => response.json())
    // .then(function(json){
    //     return json;
    // });
    //バブルがつくられた回数
    var created_count = -1;
    //
    //<<未実装　おわり>>
    console.log("Start");
    init();

    //TODO
    var stack = Composites.stack(20, 20, 10, 4, 0, 0, function(x, y) {

        var name_list = json_data;
       

        function create_circle(x,y,name){
            return Bodies.circle(x, y, 46, {
                density: 0.001,
                frictionAir: 0.3,
                restitution: 0.03,
                friction: 0.05,
                render: {
                    sprite: {
                        //img/${name}.png
                        //{{url_for('static', filename='ayrton_senna_movie_wallpaper_by_bashgfx-d4cm6x6.jpg')}}
                        texture: `${url} + ${name}.png`
                    }
                }
            });
            }

        //配列の要素以上に処理を行わない
        if(created_count+1 >= name_list.length){
            return;
        }else{
            created_count = created_count+1;
            return create_circle(x,y,name_list[created_count]);
        }
    });

    World.add(world, stack);

    // add mouse control
    var mouse = Mouse.create(render.canvas),
        mouseConstraint = MouseConstraint.create(engine, {
            mouse: mouse,
            constraint: {
                stiffness: 0.2,
                render: {
                    visible: false
                }
            }
        });

    World.add(world, mouseConstraint);

    // keep the mouse in sync with rendering
    render.mouse = mouse;

    // fit the render viewport to the scene
    Render.lookAt(render, {
        min: { x: 0, y: 0 },
        max: { x: 800, y: 600 }
    });

    // context for MatterTools.Demo
    return {
        engine: engine,
        runner: runner,
        render: render,
        canvas: render.canvas,
        stop: function() {
            Matter.Render.stop(render);
            Matter.Runner.stop(runner);
        }
    };
};

if (typeof module !== 'undefined') {
    module.exports = Example[Object.keys(Example)[0]]};