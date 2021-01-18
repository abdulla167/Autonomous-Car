import 'dart:async';
import 'dart:collection';
import 'dart:math' as _math;

import 'package:control_pad/models/gestures.dart';
import 'package:control_pad/models/pad_button_item.dart';
import 'package:control_pad/views/circle_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import 'center_button.dart';

typedef PadButtonPressedCallback = void Function(
    int buttonIndex, Gestures gesture);

class PadButtonsView extends StatelessWidget {
  /// [size] optional parameter, space for background circle of all padd buttons. It will be
  /// recalculated for pad buttons size.
  ///
  /// Default value is calculated according to screen size.
  final double size;

  /// List of pad buttons, default contains 4 buttons
  final List<PadButtonItem> buttons;

  final CenterButton centerButton;

  /// [padButtonPressedCallback] contains information which button(index) was
  /// used by user and what gesture was done on it.
  final PadButtonPressedCallback padButtonPressedCallback;

  /// [buttonsStateMap] contains current colors of each button.
  final Map<int, Color> buttonsStateMap = HashMap<int, Color>();

  /// [buttonsPadding] optional parameter to ad paddings for buttons.
  final double buttonsPadding;

  /// [backgroundPadButtonsColor] optional parameter, when set it shows circle.
  final Color backgroundPadButtonsColor;

  Timer timer;

  PadButtonsView({
    this.size,
    this.buttons = const [
      PadButtonItem(
          index: 1,
          buttonIcon: Icon(
            Icons.arrow_forward,
          )),
      PadButtonItem(
          index: 2,
          buttonIcon: Icon(Icons.arrow_downward),
          pressedColor: Colors.red),
      PadButtonItem(
          index: 3,
          buttonIcon: Icon(
            Icons.arrow_back,
          ),
          pressedColor: Colors.green),
      PadButtonItem(
          index: 0,
          buttonIcon: Icon(
            Icons.arrow_upward,
          ),
          pressedColor: Colors.yellow),
    ],
    this.centerButton,
    this.padButtonPressedCallback,
    this.buttonsPadding = 0,
    this.backgroundPadButtonsColor = Colors.transparent,
  }) : assert(buttons != null && buttons.isNotEmpty) {
    buttons.forEach(
        (button) => buttonsStateMap[button.index] = button.backgroundColor);
  }

  @override
  Widget build(BuildContext context) {
    double actualSize = size != null
        ? size
        : _math.min(MediaQuery.of(context).size.width,
                MediaQuery.of(context).size.height) *
            0.5;
    double innerCircleSize = actualSize / 4;

    return Center(
        child: Stack(children: createButtons(innerCircleSize, actualSize)));
  }

  List<Widget> createButtons(double innerCircleSize, double actualSize) {
    List<Widget> list = List();
    list.add(CircleView.padBackgroundCircle(
        actualSize,
        backgroundPadButtonsColor,
        backgroundPadButtonsColor != Colors.transparent
            ? Colors.black45
            : Colors.transparent,
        backgroundPadButtonsColor != Colors.transparent
            ? Colors.black12
            : Colors.transparent));

    for (var i = 0; i < buttons.length; i++) {
      var padButton = buttons[i];
      list.add(createPositionedButtons(
        padButton,
        actualSize,
        i,
        innerCircleSize,
      ));
    }
    if (centerButton != null){
      list.add(Positioned(
          top: actualSize / 2 - centerButton.height / 2, left: actualSize / 2 - centerButton.width / 2, child: centerButton.widget));
    }
    return list;
  }

  Positioned createPositionedButtons(PadButtonItem paddButton,
      double actualSize, int index, double innerCircleSize) {
    return Positioned(
      child: StatefulBuilder(builder: (context, setState) {
        return GestureDetector(
          onTap: () {
            _processGestureTap(paddButton, Gestures.TAP);
          },
          onTapUp: (details) {
            // _processGestureTap(paddButton, Gestures.TAPUP);
            Future.delayed(const Duration(milliseconds: 50), () {
              setState(() => buttonsStateMap[paddButton.index] =
                  paddButton.backgroundColor);
            });
          },
          onTapDown: (details) {
            // _processGestureTap(paddButton, Gestures.TAPDOWN);
            setState(() =>
                buttonsStateMap[paddButton.index] = paddButton.pressedColor);
          },
          onTapCancel: () {
            // _processGestureTap(paddButton, Gestures.TAPCANCEL);
            setState(() =>
                buttonsStateMap[paddButton.index] = paddButton.backgroundColor);
          },
          onLongPressStart: (details) {
            // _processGesture(paddButton, Gestures.LONGPRESSSTART);
            setState(() =>
                buttonsStateMap[paddButton.index] = paddButton.pressedColor);
          },
          onLongPress: () {
            timer = Timer.periodic(
                Duration(milliseconds: 320),
                (_) => padButtonPressedCallback(
                    paddButton.index, Gestures.LONGPRESSSTART));
            _processGesture(paddButton, Gestures.LONGPRESS);
          },
          onLongPressEnd: (_) {
            timer?.cancel();
          },
          onLongPressUp: () {
            _processGesture(paddButton, Gestures.LONGPRESSUP);
            setState(() =>
                buttonsStateMap[paddButton.index] = paddButton.backgroundColor);
          },
          child: Padding(
            padding: EdgeInsets.all(buttonsPadding),
            child: CircleView.padButtonCircle(
                innerCircleSize,
                buttonsStateMap[paddButton.index],
                paddButton.buttonImage,
                paddButton.buttonIcon,
                paddButton.buttonText),
          ),
        );
      }),
      top: _calculatePositionYOfButton(index, innerCircleSize, actualSize),
      left: _calculatePositionXOfButton(index, innerCircleSize, actualSize),
    );
  }

  void _processGesture(PadButtonItem button, Gestures gesture) {
    if (padButtonPressedCallback != null) {
      padButtonPressedCallback(button.index, gesture);
    }
  }

  void _processGestureTap(PadButtonItem button, Gestures gesture) {
    if (padButtonPressedCallback != null && gesture == Gestures.TAP) {
      padButtonPressedCallback(button.index, gesture);
    }
  }

  double _calculatePositionXOfButton(
      int index, double innerCircleSize, double actualSize) {
    double degrees = 360 / buttons.length * index;
    double lastAngleRadians = (degrees) * (_math.pi / 180.0);

    var rBig = actualSize / 2;
    var rSmall = (innerCircleSize + 2 * buttonsPadding) / 2;

    return (rBig - rSmall) + (rBig - rSmall) * _math.cos(lastAngleRadians);
  }

  double _calculatePositionYOfButton(
      int index, double innerCircleSize, double actualSize) {
    double degrees = 360 / buttons.length * index;
    double lastAngleRadians = (degrees) * (_math.pi / 180.0);
    var rBig = actualSize / 2;
    var rSmall = (innerCircleSize + 2 * buttonsPadding) / 2;

    return (rBig - rSmall) + (rBig - rSmall) * _math.sin(lastAngleRadians);
  }
}


