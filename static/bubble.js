(function() {

    var Engine = Matter.Engine;
    var World = Matter.World;
    var Bodies = Matter.Bodies;
    var Body = Matter.Body;
    var MouseConstraint = Matter.MouseConstraint;
    var Render = Matter.Render;
    var Events = Matter.Events;
    var Composites = Matter.Composites;
    var engine = Engine.create(document.body, {
      render: {
        options: {
          width: 810,
          height: 600,
          pixelRatio: 1,
          background: '#000000',
          wireframeBackground: '#222',
          hasBounds: false,
          enabled: false,
          wireframes: false,
          showSleeping: false,
          showDebug: true,
          showBroadphase: true,
          showBounds: false,
          showVelocity: false,
          showCollisions: false,
          showSeparations: false,
          showAxes: false,
          showPositions: false,
          showAngleIndicator: false,
          showIds: false,
          showShadows: false,
          showVertexNumbers: false,
          showConvexHulls: false,
          showInternalEdges: false
        }
      }
    });
  
    // isStatic:静的(完全固定) 地面と棒を追加
    var ground0 = Bodies.rectangle(0, 610, 1, 1000, { isStatic: true });
    // var ground1 = Bodies.rectangle(100, 610, 1, 1000, { isStatic: true });
    // var ground2 = Bodies.rectangle(200, 610, 1, 1000, { isStatic: true });
    // var ground3 = Bodies.rectangle(300, 610, 1, 1000, { isStatic: true });
    // var ground4 = Bodies.rectangle(400, 610, 1, 1000, { isStatic: true });
    // var ground5 = Bodies.rectangle(500, 610, 1, 1000, { isStatic: true });
    // var ground6 = Bodies.rectangle(600, 610, 1, 1000, { isStatic: true });
    // var ground7 = Bodies.rectangle(700, 610, 1, 1000, { isStatic: true });
    var ground8 = Bodies.rectangle(800, 610, 1, 1000, { isStatic: true });
    var ground9 = Bodies.rectangle(400, 610, 810, 60, { isStatic: true });
    var group = Body.nextGroup(true),
          particleOptions = { friction: 0.00001, collisionFilter: { group: group }, render: { visible: false }},
          constraintOptions = { stiffness: 0.06 };

  
    // クリックしたら操作できる。
    var mousedrag = MouseConstraint.create(engine, {
        element: document.body, 
        constraint: {
          render: {
            strokeStyle: "rgba(0,0,0,0)" //マウスの動きを表示する(白)
          }
        }
      });
  
    World.add(engine.world, [ground0, ground8, ground9, mousedrag]);
  
    for (var i = 0; i < 10; i++) {
      var rnd = parseInt(Math.random() * 10);
      var x = 320 + rnd * 10;
      var y = 0 - rnd * 120;
      rnd2 = parseInt(Math.random() * 640);
      var x2 = rnd2;
      var y2 = 0 - rnd2 * 2;
  
      World.add(engine.world, [
          Bodies.circle(x, y, 49, { //ボールを追加
              density: 0.0005, // 密度
              frictionAir: 0.06, // 空気抵抗
              restitution: 1, // 弾力性
              friction: 0.01, // 本体の摩擦
              render: { //ボールのレンダリング
            options: {
              showAngleIndicator: false,
              showIds: false,
              showShadows: false,
              showVertexNumbers: false,
            }
              },
              timeScale: 1.5 //時間の倍率を設定(1で1倍速)
          }),
      ]);
  
    }
    function create_bubble(bubble_size){
        var rnd = parseInt(Math.random() * 10);
        var x = 320 + rnd * 10;
        var y = 0 - rnd * 120;

        World.add(engine.world, [
            Bodies.circle(x, y, bubble_size, { //ボールを追加
                density: 0.0005, // 密度
                frictionAir: 0.06, // 空気抵抗
                restitution: 1, // 弾力性
                friction: 0.01, // 本体の摩擦
                render: { //ボールのレンダリング
              options: {
                showAngleIndicator: false,
                showIds: false,
                showShadows: false,
                showVertexNumbers: false,
              }
                },
                timeScale: 1.5 //時間の倍率を設定(1で1倍速)
            }),
        ]);
    }
    create_bubble(100)
    //現在の日付とTODOの日付を比較して大きさを決定
    //一つづつサイズを決定して作成
    //

  // 物理シミュレーションを実行
  Engine.run(engine);
  })();