//
//  SafariExtensionHandler.swift
//  AutoCap Extension
//
//  Created by Kamran Ahmed on 11/22/21.
//

import SafariServices

class SafariExtensionHandler: SFSafariExtensionHandler {
    
    override func messageReceived(withName messageName: String, from page: SFSafariPage, userInfo: [String : Any]?) {
        // let url = URL(string: "http://35.192.169.60.sslip.io/api/models")!
        // let task = URLSession.shared.dataTask(with: url) {(data, response, error) in
        //     guard let data = data else {
        //         page.dispatchMessageToScript(withName: "getData", userInfo: ["error": error?.localizedDescription ?? ""])
        //         return
        //      }
        //      let json = try? JSONSerialization.jsonObject(with: data, options: [])
        //         if let json = json as? [String: Any] {
        //             page.dispatchMessageToScript(withName: "getData", userInfo: json)
        //         }
        // }
        // task.resume()
        page.dispatchMessageToScript(withName: "getData", userInfo: userInfo)
    }

    override func toolbarItemClicked(in window: SFSafariWindow) {
        // This method will be called when your toolbar item is clicked.
        NSLog("The extension's toolbar item was clicked")
    }
    
    override func validateToolbarItem(in window: SFSafariWindow, validationHandler: @escaping ((Bool, String) -> Void)) {
        // This is called when Safari's state changed in some way that would require the extension's toolbar item to be validated again.
        validationHandler(true, "")
    }
    
    override func popoverViewController() -> SFSafariExtensionViewController {
        return SafariExtensionViewController.shared
    }

    override func beginRequest(with context: NSExtensionContext) {
        let item = context.inputItems[0] as! NSExtensionItem
        let message = item.userInfo?[SFExtensionMessageKey]

        let response = NSExtensionItem()
        response.userInfo = [ SFExtensionMessageKey: [ "Response to": message ] ]
            
        context.completeRequest(returningItems: [response], completionHandler: nil)
    }

}
