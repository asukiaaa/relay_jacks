import cadquery as cq
from Helpers import show

clealance = 0.2
narrowClearance = clealance / 2
holeClealance = 0.7
relaysPcbNumber = 3
relaysPcbWidth = 30.5
relaysPcbLength = 36.0
relaysPcbThickness = 1.6
relaysPcbHolePositions = ((-5.2, 3.5), (5.2, 3.5))
relaysPcbAudioXPositions = (-10.2, 0, 10.2)
relaysPcbHoleCenterHeight = 2.0
audioHoleCenterHeight = 2.55
audioHoleRadius = 5.0 / 2
proMicroWidth = 18.0
proMicroLength = 33.0
proMicroThickness = 1.6
proMicroUSBHeight = 2.5
proMicroUSBWidth = 7.5
proMicroHolderThickness = 1.0
proMicroHolderLowHeight = 4.0
proMicroHolderCoverLength = 2.6
relaysPcbToUsbClealance = 2.0
wireRadius = 3.0 / 2
mountingHoleHeight = 3.5
mountingHoleRadius = 2.3 / 2
mountSupporerThickness = 1.0
boxThickness = 1.0
boxInnerWidth = (relaysPcbWidth + clealance) * relaysPcbNumber + clealance \
    + relaysPcbToUsbClealance \
    + proMicroThickness + proMicroUSBHeight \
    + proMicroHolderThickness * 2 + clealance * 2
boxInnerLength = relaysPcbLength + clealance * 2
boxInnerHeight = proMicroWidth + clealance * 2
boxOuterWidth = boxInnerWidth + boxThickness * 2
boxOuterLength = boxInnerLength + boxThickness * 2
boxOuterHeight = boxInnerHeight + boxThickness * 2

body = cq.Workplane("XY").box(boxInnerWidth, boxInnerLength, boxInnerHeight) \
    .faces(">Z").shell(boxThickness) \
    .translate((boxInnerWidth / 2,
                boxInnerLength / 2,
                boxInnerHeight / 2))

moutingHoleBase = cq.Workplane("XY").circle(mountingHoleRadius + 1) \
    .extrude(mountingHoleHeight)
moutingHole = cq.Workplane("XY").circle(mountingHoleRadius) \
    .extrude(mountingHoleHeight + boxThickness)
audioHole = cq.Workplane("XZ").circle(audioHoleRadius).extrude(boxThickness)
mountSupporterY = cq.Workplane("XY").box(mountSupporerThickness,
                                         boxInnerLength * 2 / 3,
                                         mountingHoleHeight)
mountSupporterXWidth = boxInnerWidth - proMicroThickness - proMicroUSBHeight \
    - clealance * 2 - relaysPcbToUsbClealance
mountSuporterX = cq.Workplane("XY").box(mountSupporterXWidth,
                                        mountSupporerThickness,
                                        mountingHoleHeight)
pcbCenterY = clealance + relaysPcbLength / 2
body = body.union(mountSuporterX.translate((mountSupporterXWidth / 2,
                                            pcbCenterY +
                                            relaysPcbHolePositions[0][1],
                                            mountingHoleHeight / 2)))

for i in range(0, relaysPcbNumber):
    pcbCenterX = (relaysPcbWidth + clealance) * i \
        + clealance + relaysPcbWidth / 2
    for (x, y) in relaysPcbHolePositions:
        body = body.union(moutingHoleBase.translate((pcbCenterX + x,
                                                     pcbCenterY + y,
                                                     0)))
        body = body.union(mountSupporterY.translate((pcbCenterX + x,
                                                     boxInnerLength / 2,
                                                     mountingHoleHeight / 2)))
        body.cut(moutingHole.translate((pcbCenterX + x,
                                        pcbCenterY + y,
                                        - boxThickness)))
    for x in relaysPcbAudioXPositions:
        body.cut(audioHole.translate((
            pcbCenterX + x,
            boxInnerLength + boxThickness,
            mountingHoleHeight + relaysPcbThickness + audioHoleCenterHeight)))
usbHoleWidth = proMicroUSBHeight + holeClealance * 2
usbHoleHeight = proMicroUSBWidth + holeClealance * 2
usbHoleBottomZ = (boxInnerHeight - usbHoleHeight) / 2
usbBodyHoleHeight = boxInnerHeight - usbHoleBottomZ
usbHoleCenterX = boxInnerWidth - proMicroThickness - clealance - \
    mountSupporerThickness - usbHoleWidth / 2
usbHole = cq.Workplane('XY').box(usbHoleWidth,
                                 boxThickness,
                                 usbBodyHoleHeight)
body.cut(usbHole.translate((
    usbHoleCenterX,
    boxInnerLength + boxThickness / 2,
    boxInnerHeight - usbBodyHoleHeight / 2)))

proMicroHolderLowY = cq.Workplane("XY").box(proMicroHolderThickness,
                                            proMicroHolderCoverLength,
                                            proMicroHolderLowHeight)
proMicroHolderHighY = cq.Workplane("XY").box(proMicroHolderThickness,
                                             proMicroHolderCoverLength,
                                             boxInnerHeight)
proMicroHolderXWidth = \
    proMicroThickness + proMicroHolderThickness * 2 + clealance * 2
proMicroHolderX = cq.Workplane("XY") \
    .box(proMicroHolderXWidth, proMicroHolderThickness, boxInnerHeight)

proMicroHolderYOuterX = boxInnerWidth - proMicroHolderThickness / 2
proMicroHolderYInnerX = proMicroHolderYOuterX \
    - clealance * 2 - proMicroThickness - proMicroHolderThickness
proMicroHolderYUpperY = boxInnerLength - proMicroHolderCoverLength / 2
proMicroHolderYLowerY = \
    boxInnerLength - proMicroLength - narrowClearance * 2 + \
    proMicroHolderCoverLength / 2

body = body.union(proMicroHolderLowY.translate((
    proMicroHolderYInnerX,
    proMicroHolderYUpperY,
    proMicroHolderLowHeight / 2)))
body = body.union(proMicroHolderHighY.translate((
    proMicroHolderYOuterX,
    proMicroHolderYUpperY,
    boxInnerHeight / 2)))
body = body.union(proMicroHolderHighY.translate((
    proMicroHolderYInnerX,
    proMicroHolderYLowerY,
    boxInnerHeight / 2)))
body = body.union(proMicroHolderHighY.translate((
    proMicroHolderYOuterX,
    proMicroHolderYLowerY,
    boxInnerHeight / 2)))
body = body.union(proMicroHolderX.translate((
    boxInnerWidth - proMicroHolderXWidth / 2,
    boxInnerLength - proMicroLength - narrowClearance * 2 -
    proMicroHolderThickness / 2,
    boxInnerHeight / 2)))

wireHoleWidth = (wireRadius + narrowClearance) * 2
wireHole = cq.Workplane('XY') \
    .box(wireHoleWidth, boxThickness, usbHoleBottomZ) \
    .faces('<Z').edges('|Y').fillet(wireRadius) \
    .translate((proMicroHolderYInnerX - proMicroHolderThickness / 2 -
                wireHoleWidth / 2,
                boxInnerLength + boxThickness / 2,
                usbHoleBottomZ / 2))
body.cut(wireHole)

testZoneWidth = boxOuterWidth * 2 / 3
testZoneLength = boxOuterLength
testZoneHiehgt = boxOuterHeight
testZone = cq.Workplane('XY') \
    .box(testZoneWidth, testZoneLength, testZoneHiehgt) \
    .translate((testZoneWidth / 2 - boxThickness,
                boxInnerLength + boxThickness - testZoneLength / 2,
                boxInnerHeight / 2))
body = body.cut(testZone)

show(body)
