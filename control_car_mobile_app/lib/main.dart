import 'dart:math';

import 'package:control_car/center_button.dart';
import 'package:control_pad/models/pad_button_item.dart';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/io.dart';

import 'pad.dart';

void main() {
  runApp(ExampleApp());
}

class ExampleApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Car Control',
      theme: ThemeData.dark(),
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  double precession = 30;
  bool connected = false;
  bool connecting = false;
  String _RFID = '';
  bool mode = true;

  List<Color> colors = const [
    Colors.white,
    Colors.red,
    Colors.blueAccent,
    Colors.indigo
  ];

  Color _RFIDColor ;

  Random random = Random();

  IOWebSocketChannel controller = null;
  TextEditingController textEditingController = TextEditingController();
  String host = '';

  List<PadButtonItem> buttons = [
    PadButtonItem(
        index: 2,
        buttonImage: Image.asset("assets/right.png"),
        pressedColor: Colors.green),
    PadButtonItem(
        index: 6,
        buttonImage: Image.asset("assets/down-right.png"),
        pressedColor: Colors.orange),
    PadButtonItem(
        index: 3,
        buttonImage: Image.asset("assets/down.png"),
        pressedColor: Colors.red),
    PadButtonItem(
        index: 7,
        buttonImage: Image.asset("assets/down-left.png"),
        pressedColor: Colors.indigo),
    PadButtonItem(
        index: 4,
        buttonImage: Image.asset("assets/left.png"),
        pressedColor: Colors.yellow),
    PadButtonItem(
        index: 8,
        buttonImage: Image.asset("assets/up-left.png"),
        pressedColor: Colors.deepOrange),
    PadButtonItem(
      index: 1,
      buttonImage: Image.asset("assets/up.png"),
    ),
    PadButtonItem(
        index: 5,
        buttonImage: Image.asset(
          "assets/up-right.png",
        ),
        pressedColor: Colors.white),
  ];

  @override
  void initState() {
    super.initState();
    textEditingController.addListener(() {
      host = textEditingController.text;
    });
    _RFIDColor = colors[0];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Car Control'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Card(
              child: ListTile(
                title: Text("RFID:"),
                trailing: Text(
                  _RFID,
                  style: TextStyle(color: _RFIDColor, fontSize: 18),
                ),
              ),
            ),
            Row(
              children: [
                Flexible(
                  child: Container(
                    margin: EdgeInsets.all(10),
                    child: TextFormField(
                      controller: textEditingController,
                      decoration: InputDecoration(
                        labelText: "URL",
                        border: OutlineInputBorder(),
                      ),
                    ),
                  ),
                ),
                Container(
                  margin: EdgeInsets.all(10),
                  child: RaisedButton(
                    child: Text(
                      "Connect",
                      style: TextStyle(color: Colors.white),
                    ),
                    color: Colors.redAccent,
                    onPressed: () {
                      try {
                        controller = IOWebSocketChannel.connect(host);
                        setState(() {
                          connecting = true;
                        });
                        controller.stream.listen((event) {
                          if (event == "c") {
                            setState(() {
                              connecting = false;
                              connected = true;
                            });
                          } else if (event == "96 1D 17 7E") {
                            setState(() {
                              _RFID = event.toString();
                              _RFIDColor = colors[random.nextInt(3)];
                            });
                          }
                        }, onDone: () {
                          setState(() {
                            connecting = false;
                            connected = false;
                          });
                        });
                      } catch (e) {
                        setState(() {
                          connecting = false;
                          connected = false;
                        });
                      }
                    },
                  ),
                )
              ],
            ),
            SizedBox(
              height: 80,
            ),
            PadButtonsView(
              size: 250,
              buttons: buttons,
              padButtonPressedCallback: (index, _) {
                // print("deg: $degree, distance: $distance");
                sendData(index);
              },
              centerButton: CenterButton(
                width: 60,
                height: 60,
                widget: Container(
                  width: 60,
                  height: 60,
                  child: Center(
                    child: GestureDetector(
                      child: Text(
                        mode ? "Auto" : "Manual",
                        style: TextStyle(fontWeight: FontWeight.w700),
                      ),
                      onTap: () {
                        setState(() {
                          mode = !mode;
                          if (mode == false) {
                            controller.sink.add("auto");
                          }
                        });
                      },
                    ),
                  ),
                  decoration: BoxDecoration(
                    color: Colors.grey,
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: Colors.black26,
                      width: 2.0,
                      style: BorderStyle.solid,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.grey,
                        spreadRadius: 4.0,
                        blurRadius: 4.0,
                      )
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: connected ? Colors.redAccent : Colors.grey,
        onPressed: () {},
        child: connecting
            ? CircularProgressIndicator()
            : Icon(connected ? Icons.wifi : Icons.wifi_off),
      ),
    );
  }

  void sendData(int index) {
    switch (index) {
      case 1:
        print("F");
        // connection.output.add(utf8.encode("0"));
        controller?.sink?.add("F");
        break;
      case 2:
        print("R");
        controller?.sink?.add("R");
        // connection?.output?.add(utf8.encode("2"));
        break;
      case 3:
        print("B");
        // connection?.output?.add(utf8.encode("4"));
        controller?.sink?.add("B");
        break;
      case 4:
        print("L");
        // connection?.output?.add(utf8.encode("6"));
        controller?.sink?.add("L");
        break;
      case 5:
        print("FR");
        // connection?.output?.add(utf8.encode("6"));
        controller?.sink?.add("G");
        break;
      case 6:
        print("BR");
        // connection?.output?.add(utf8.encode("6"));
        controller?.sink?.add("H");
        break;
      case 7:
        print("BL");
        // connection?.output?.add(utf8.encode("6"));
        controller?.sink?.add("I");
        break;
      case 8:
        print("FL");
        // connection?.output?.add(utf8.encode("6"));
        controller?.sink?.add("J");
        break;
    }
  }
}
