// macOS AVFoundation encoder for silent, compatible H.264 portfolio loops.
import Foundation
import AppKit
import AVFoundation
import CoreVideo
import CoreMedia
let out = URL(fileURLWithPath:CommandLine.arguments[1],isDirectory:true)
let slugs=["parkwise","credence","scholarship-aid","smarthealth","cinematic","scholarai","checkstyle","gson","java-pathfinder"]
let width=1280, height=720, fps:Int32=24
func load(_ name:String)->CGImage {
    let image=NSImage(contentsOf:out.appendingPathComponent(name+".jpg"))!
    return image.cgImage(forProposedRect:nil,context:nil,hints:nil)!
}
func encode(_ name:String,images:[CGImage],seconds:Int) throws {
 let url=out.appendingPathComponent(name+".mp4")
 try? FileManager.default.removeItem(at:url)
 let writer=try AVAssetWriter(outputURL:url,fileType:.mp4)
 let settings:[String:Any]=[AVVideoCodecKey:AVVideoCodecType.h264,AVVideoWidthKey:width,AVVideoHeightKey:height,AVVideoCompressionPropertiesKey:[AVVideoAverageBitRateKey:2200000,AVVideoProfileLevelKey:AVVideoProfileLevelH264HighAutoLevel,AVVideoMaxKeyFrameIntervalKey:48,AVVideoAllowFrameReorderingKey:false]]
 let input=AVAssetWriterInput(mediaType:.video,outputSettings:settings)
 input.expectsMediaDataInRealTime=false
 let attributes:[String:Any]=[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32ARGB,kCVPixelBufferWidthKey as String:width,kCVPixelBufferHeightKey as String:height,kCVPixelBufferCGImageCompatibilityKey as String:true,kCVPixelBufferCGBitmapContextCompatibilityKey as String:true]
 let adaptor=AVAssetWriterInputPixelBufferAdaptor(assetWriterInput:input,sourcePixelBufferAttributes:attributes)
 writer.add(input);writer.shouldOptimizeForNetworkUse=true
 guard writer.startWriting() else {throw writer.error!}
 writer.startSession(atSourceTime:.zero)
 let frames=seconds*Int(fps)
 for i in 0..<frames {
  while !input.isReadyForMoreMediaData { Thread.sleep(forTimeInterval:0.004) }
  var pixel:CVPixelBuffer?
  CVPixelBufferPoolCreatePixelBuffer(kCFAllocatorDefault,adaptor.pixelBufferPool!,&pixel)
  let buffer=pixel!
  CVPixelBufferLockBaseAddress(buffer,[])
  let context=CGContext(data:CVPixelBufferGetBaseAddress(buffer),width:width,height:height,bitsPerComponent:8,bytesPerRow:CVPixelBufferGetBytesPerRow(buffer),space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.noneSkipFirst.rawValue)!
  context.setFillColor(CGColor(red:0.025,green:0.035,blue:0.05,alpha:1));context.fill(CGRect(x:0,y:0,width:width,height:height))
  let t=Double(i)/Double(frames)
  let scaled=t*Double(images.count)
  let idx=min(images.count-1,Int(scaled))
  let phase=scaled-Double(idx)
  // A full cosine cycle joins smoothly for single-image loops.
  let zoom=1.0+0.025*(1-cos(phase*2*Double.pi))/2
  let w=Double(width)*zoom,h=Double(height)*zoom
  context.interpolationQuality = .high
  context.draw(images[idx],in:CGRect(x:(Double(width)-w)/2,y:(Double(height)-h)/2,width:w,height:h))
  if images.count>1 && phase>0.82 {
    context.setAlpha((phase-0.82)/0.18)
    context.draw(images[(idx+1)%images.count],in:CGRect(x:0,y:0,width:width,height:height))
    context.setAlpha(1)
  }
  CVPixelBufferUnlockBaseAddress(buffer,[])
  guard adaptor.append(buffer,withPresentationTime:CMTime(value:Int64(i),timescale:fps)) else {throw writer.error!}
 }
 input.markAsFinished()
 let sem=DispatchSemaphore(value:0)
 writer.finishWriting {sem.signal()}
 sem.wait()
 guard writer.status == .completed else {throw writer.error!}
 print("Encoded \(name).mp4")
}
for slug in slugs {try encode(slug,images:[load(slug)],seconds:4)}
try encode("showreel",images:[load("showreel")]+slugs.prefix(6).map{load($0)},seconds:21)
