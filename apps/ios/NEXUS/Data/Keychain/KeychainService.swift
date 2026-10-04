import Foundation
import Security

public protocol KeychainServiceProtocol: Sendable {
    func save(key: String, data: Data) throws
    func read(key: String) -> Data?
    func delete(key: String) throws
    func clearAll() throws
    func saveString(key: String, value: String) throws
    func readString(key: String) -> String?
}

public enum KeychainError: LocalizedError {
    case duplicateItem
    case itemNotFound
    case unhandledError(status: OSStatus)
    case dataConversionFailed

    public var errorDescription: String? {
        switch self {
        case .duplicateItem:
            return "The item already exists in the Keychain."
        case .itemNotFound:
            return "The item was not found in the Keychain."
        case .unhandledError(let status):
            return "Keychain operation failed with OSStatus \(status)."
        case .dataConversionFailed:
            return "Failed to convert between Data and String."
        }
    }
}

nonisolated public final class NexusKeychainService: KeychainServiceProtocol, @unchecked Sendable {
    public static let shared = NexusKeychainService()
    
    private let serviceName: String
    private let accessGroup: String?

    public init(serviceName: String = "com.nexus.app", accessGroup: String? = nil) {
        self.serviceName = serviceName
        self.accessGroup = accessGroup
    }

    public func save(key: String, data: Data) throws {
        // Delete any existing item first to ensure clean upsert
        _ = try? delete(key: key)

        var query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock
        ]

        if let accessGroup = accessGroup {
            query[kSecAttrAccessGroup as String] = accessGroup
        }

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.unhandledError(status: status)
        }
    }

    public func read(key: String) -> Data? {
        var query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        if let accessGroup = accessGroup {
            query[kSecAttrAccessGroup as String] = accessGroup
        }

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess, let data = result as? Data else {
            return nil
        }
        return data
    }

    public func delete(key: String) throws {
        var query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key
        ]

        if let accessGroup = accessGroup {
            query[kSecAttrAccessGroup as String] = accessGroup
        }

        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unhandledError(status: status)
        }
    }

    public func clearAll() throws {
        var query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName
        ]

        if let accessGroup = accessGroup {
            query[kSecAttrAccessGroup as String] = accessGroup
        }

        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unhandledError(status: status)
        }
    }

    public func saveString(key: String, value: String) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.dataConversionFailed
        }
        try save(key: key, data: data)
    }

    public func readString(key: String) -> String? {
        guard let data = read(key: key) else { return nil }
        return String(data: data, encoding: .utf8)
    }
}
