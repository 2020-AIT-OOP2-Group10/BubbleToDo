var Example = Example || {};

//本番は変える
var url = "http://127.0.0.1:5000";

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
        element: document.getElementById("stage"),
        engine: engine,
        options: {
            width: 600,
            height: 600,
            background: '#fff',
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
        //Matter.Bodies.rectangle(x, y, width, height, [options])
        //上
        Bodies.rectangle(400, -100, 900.5 + offset, 40.5, options),
        //下
        Bodies.rectangle(400, 700, 900.5 + offset, 40.5, options),
        //右
        Bodies.rectangle(800 + offset, 300, 50.5, 900.5 + 2 * offset, options),
        //左
        Bodies.rectangle(-offset, 300, 50.5, 900.5 + 2 * offset, options)
    ]);
    
    var created_count = 0;

    //JSONデータをフェッチ
    fetch("/get").then(response => {
        response.json().then((data) => {

            var stack = Composites.stack(20, 20, 10, 4, 0, 0, function(x, y) {
                
                for (let i = 0;i < data.length;i++){
                    if (created_count == i) {
                        created_count += 1
                        //data[i]["size"] == 読み込む画像の横幅
                        return Bodies.circle(x, y, data[i]["size"]/2, {
                            density: 0.001,
                            frictionAir: 0.3,
                            restitution: 0.03,
                            friction: 0.05,
                            render: {
                                sprite: {
                                    //画像貼り付け(テクスチャ)
                                    texture: `${url}/upload_img/${data[i]["content"]}.png`
                                }
                            }
                        });
                    }
                }
            });

            World.add(world, stack);

        })
    })


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