import cadquery as cq
from Helpers import show

clealance = 0.2
narrowClearance = clealance / 2
holeClealance = 0.5
relaysPcbNumber = 3
relaysPcbWidth = 32.0
relaysPcbLength = 33.0
relaysPcbThickness = 1.6
relaysPcbHolePositions = ((-5.5, 3.5), (5.5, 3.5))
relaysPcbAudioXPositions = (-11.0, 0, 11.0)
relaysPcbHoleCenterHeight = 2.0
relayPcbToPcbClearance = 1.0
audioHoleCenterHeight = 2.55
audioHoleRadius = 6.0 / 2
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
mountingHoleHeight = 10.5
mountingHoleRadius = 2.3 / 2
mountSupporerThickness = 1.0
hookWidth = 4.0
hookHeight = 1.5
hookConnectionLength = 1.5
coverMountHoleRadius = 2.8 / 2
coverMountHoleCenterHeight = coverMountHoleRadius * 2
coverMountHoleLength = 10.0
coverMountThickness = 1.0
boxThickness = 1.5
boxInnerWidth = (relaysPcbWidth + relayPcbToPcbClearance) * relaysPcbNumber \
    - relayPcbToPcbClearance + clealance * 2 \
    + relaysPcbToUsbClealance \
    + proMicroThickness + proMicroUSBHeight \
    + proMicroHolderThickness * 2 + clealance * 2
boxInnerLength = relaysPcbLength + clealance * 2
boxInnerHeight = proMicroWidth + clealance * 2
boxOuterWidth = boxInnerWidth + boxThickness * 2
boxOuterLength = boxInnerLength + boxThickness * 2
boxOuterHeight = boxInnerHeight + boxThickness * 2
wireFixPillowRadius = 3.0 / 2
wireFixPollowHeight = wireRadius * 3
wireFixPillowPositions = ((boxInnerWidth - 3.0, boxInnerLength),
                          (boxInnerWidth - 6.0, boxInnerLength - 6.0),
                          (boxInnerWidth - 3.0, boxInnerLength - 12.0))

# body = cq.Workplane("XY") \
#     .box(boxInnerWidth, boxInnerLength, boxInnerHeight) \
#     .faces(">Z").shell(boxThickness) \
#     .translate((boxInnerWidth / 2,
#                 boxInnerLength / 2,
#                 boxInnerHeight / 2))

cutBox = cq.Workplane("XY") \
    .box(boxInnerWidth, boxOuterLength, boxOuterHeight)

body = cq.Workplane("XY").box(boxOuterWidth, boxOuterLength, boxOuterHeight) \
    .edges("|X or |Y or |Z").fillet(boxThickness) \
    .cut(cutBox.translate((0, - boxThickness, boxThickness))) \
    .translate((boxInnerWidth / 2,
                boxInnerLength / 2,
                boxInnerHeight / 2))

moutingHoleBase = cq.Workplane("XY").circle(mountingHoleRadius + 1) \
    .extrude(mountingHoleHeight)
moutingHole = cq.Workplane("XY").circle(mountingHoleRadius) \
    .extrude(mountingHoleHeight + boxThickness)
audioHole = cq.Workplane("XZ").circle(audioHoleRadius).extrude(boxThickness)
mountSupporterY = cq.Workplane("XY").box(mountSupporerThickness,
                                         boxInnerLength,
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
hookHoleHeight = hookHeight + clealance * 2
hookHole = cq.Workplane("XY").box(hookWidth + clealance * 2,
                                  boxThickness,
                                  hookHoleHeight)
coverMountHoleBase = cq.Workplane("XZ") \
    .circle(coverMountHoleRadius + coverMountThickness) \
    .extrude(coverMountHoleLength)
coverMountHole = cq.Workplane("XZ").circle(coverMountHoleRadius) \
    .extrude(coverMountHoleLength)

for i in range(0, relaysPcbNumber):
    pcbCenterX = (relaysPcbWidth + relayPcbToPcbClearance) * i \
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
        if (x > 0):
            body.cut(hookHole.translate((pcbCenterX + x,
                                         boxInnerLength + boxThickness / 2,
                                         boxInnerHeight - hookHoleHeight / 2)))
            body = body.union(coverMountHoleBase.translate((
                pcbCenterX + x,
                coverMountHoleLength,
                coverMountHoleCenterHeight)))
            body.cut(coverMountHole.translate((
                pcbCenterX + x,
                coverMountHoleLength,
                coverMountHoleCenterHeight)))
    for x in relaysPcbAudioXPositions:
        body.cut(audioHole.translate((
            pcbCenterX + x,
            boxInnerLength + boxThickness,
            mountingHoleHeight - audioHoleCenterHeight)))
usbHoleWidth = proMicroUSBHeight + holeClealance * 2
usbHoleHeight = proMicroUSBWidth + holeClealance * 2
usbHoleBottomZ = (boxInnerHeight - usbHoleHeight) / 2
usbBodyHoleHeight = boxInnerHeight - usbHoleBottomZ + boxThickness
usbHoleCenterX = boxInnerWidth - proMicroThickness - narrowClearance - \
    mountSupporerThickness - usbHoleWidth / 2
usbHole = cq.Workplane('XY').box(usbHoleWidth,
                                 boxThickness,
                                 usbBodyHoleHeight)
body.cut(usbHole.translate((
    usbHoleCenterX,
    boxInnerLength + boxThickness / 2,
    usbHoleBottomZ + usbBodyHoleHeight / 2)))

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

wireFixPillow = cq.Workplane('XY').circle(wireFixPillowRadius) \
    .extrude(wireFixPollowHeight)
for (x, y) in wireFixPillowPositions:
    body = body.union(wireFixPillow.translate((x, y, 0)))

# testZoneWidth = boxOuterWidth * 2 / 3
# testZoneLength = boxOuterLength
# testZoneHiehgt = boxOuterHeight
# testZone = cq.Workplane('XY') \
#     .box(testZoneWidth, testZoneLength, testZoneHiehgt) \
#     .translate((testZoneWidth / 2 - boxThickness,
#                 boxInnerLength + boxThickness - testZoneLength / 2,
#                 boxInnerHeight / 2))
# body = body.cut(testZone)

show(body)
